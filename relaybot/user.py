# -*- coding: utf-8 -*-
import steam.client
import steam.client.builtins.friends

from steam.core.msg import MsgProto, Msg
from steam.core.msg.structs import ClientChatMsg
from steam.enums import EResult, EPersonaState, EFriendRelationship
from steam.enums import EChatEntryType
from steam.enums.emsg import EMsg

import logging
import os
import time

from config import config
logger = logging.getLogger(__name__)


class User(object):
    """Handles interaction with Steam, including logging in and reacting to
    events sent from Steam servers.
    """
    def __init__(self, bot, groupsinst, client):
        logger.info("Creating a User instance")

        self.client = client
        self.client.set_credential_location(os.getcwd())

        self.friends = steam.client.builtins.friends.SteamFriendlist(
            self.client)

        #This is a dictionary of group chats the bot is currently in
        #The keys are steam ids of the groups, and the values are lists of
        #steam ids of users in these group chats
        #If there is a group chat id here, it means the bot is in the chat
        #(unless the ghost chat bug happens)
        self.chats = {}

        #This is a dictionary storing information about user permissions as
        #obtained after entering group chats. Keys are steam ids, values are
        #lists of tuples where the first element is a groupid, and the second
        #element is the permission flag.
        self.permissions = {}

        self.bot = bot

        self.client.on('error', self.handle_errors)
        self.client.on('auth_code_required', self.auth_code_prompt)
        self.client.on(EMsg.ClientFriendMsgIncoming, self.on_chat_message)
        self.client.on(EMsg.ClientAccountInfo, self.on_account_info)
        self.client.on(EMsg.ClientFriendsList, self.on_client_friends_list)
        self.client.on(EMsg.ClientAddFriendResponse, self.on_friend_added)
        self.client.on(EMsg.ClientChatInvite, self.on_chat_invite)
        self.client.on(EMsg.ClientChatMsg, self.on_group_chat_msg)
        self.client.on(EMsg.ClientChatMemberInfo, self.on_chat_member_info)
        self.client.on(EMsg.ClientChatEnter, self.on_chat_enter)

        self.groups = groupsinst

        if self.client.relogin_available:
            self.client.relogin()
        else:
            self.client.login(config["STEAM_USER"], config["STEAM_PWD"])

        msg = self.client.wait_event(EMsg.ClientAccountInfo)

        self.client.wait_event(EMsg.ClientFriendsList)
        logger.info("Logged in as %s", msg[0].body.persona_name)
        logger.info("SteamID: %s", repr(self.client.steam_id))


    def change_status(self, persona_state, player_name):
        """Changes user's status according to passed value.
        Can also change profile name.
        """
        sendmsg = MsgProto(EMsg.ClientChangeStatus)
        sendmsg.body.persona_state = persona_state
        sendmsg.body.player_name = player_name

        self.client.send(sendmsg)


    def get_name_from_steamid(self, steamid):
        """Gets the profile name corresponding to a given steam id.
        """
        suser = self.client.get_user(steamid)
        if suser.name is not None:
            return suser.name
        else:
            return "<unknown>"


    def user_in_chat(self, groupid, steamid):
        """Returns True if the bot is in the group chat of the group with
        groupid, and the user with supplied steamid is also in that chat.
        """
        try:
            return steamid in [x.steam_id for x in self.chats[groupid]]
        except KeyError:
            logger.warning("user_in_group: Bot currently not in queried group"
                           " chat")
            return False


    def username_in_chat(self, groupid, username):
        """Same as user_in_chat but looks for a name instead of a steam id.
        """
        try:
            for user in self.chats[groupid]:
                if user.name == username:
                    return True
        except KeyError:
            logger.warning("username_in_group: Bot currently not in queried"
                           " group chat")
            return False


    def username_to_steamid(self, groupid, username):
        """Returns the steam id corresponding to the username (for users in a
        particular group chat).
        """
        try:
            for user in self.chats[groupid]:
                if user.name == username:
                    return user.steam_id

        except KeyError:
            logger.warning("username_in_group: Bot currently not in queried"
                           " group chat")
            return None


    def join_chat(self, chatroomid):
        """Joins a group chat given its id.
        """
        msg = Msg(EMsg.ClientJoinChat, extended=True)
        msg.body.steamIdChat = chatroomid
        self.client.send(msg)
        self.chats[chatroomid] = []


    def leave_chat(self, chatroomid):
        """Attempts to leave a group chat.
        """
        msg = Msg(EMsg.ClientChatMemberInfo, extended=True)
        msg.body.steamIdChat = chatroomid
        msg.body.type = 1 #StateChange
        msg.body.chatAction = 0x02 #Left
        msg.body.steamIdUserActedBy = self.client.steam_id
        msg.body.steamIdUserActedOn = self.client.steam_id
        self.client.send(msg)
        del self.chats[chatroomid]


    def send_group_msg(self, chatroomid, msg):
        m = Msg(EMsg.ClientChatMsg, extended=True)
        m.body.steamIdChatter = self.client.steam_id.as_64
        m.body.steamIdChatRoom = chatroomid
        m.body.ChatMsgType = 1
        m.body.text = msg
        self.client.send(m)


    def send_msg(self, steamid, msg):
        """Sends a message to a steam user.
        """
        sendmsg = MsgProto(EMsg.ClientFriendMsg)
        sendmsg.body.steamid = steamid
        sendmsg.body.chat_entry_type = 1
        sendmsg.body.message = msg
        sendmsg.body.rtime32_server_timestamp = int(time.time())

        self.client.send(sendmsg)


    @staticmethod
    def handle_errors(self, result):
        """Steam-related error callback.
        """
        logger.error("Error: %s", repr(EResult(result)))


    def auth_code_prompt(self, is_2fa, code_mismatch):
        """Handles 2-factor authentication and Steam Guard.
        """
        if code_mismatch:
            logger.error("Invalid authentication code")

        if is_2fa:
            code = raw_input("Enter Steam Mobile Authenticator code: ")
            self.client.login(config["STEAM_USER"], config["STEAM_PWD"], two_factor_code=code)
        else:
            code = raw_input("Enter Steam Guard code: ")
            self.client.login(config["STEAM_USER"], config["STEAM_PWD"], auth_code=code)


    def on_account_info(self, msg):
        """Sets status to online right after we log in and get our account
        info.
        """
        if msg is None:
            return

        logger.info("Received ClientAccountInfo")
        self.change_status(EPersonaState.Online, config["STEAM_PROFILE_NAME"])


    def on_client_friends_list(self, msg):
        """Prints the list of friends and accepts friend invites when it
        receives the ClientFriendsList event.
        """
        if msg is None:
            return
        logger.info("We have %d friends", len(self.friends))

        for friend in self.friends:
            logger.info("Friend: %s (%d)", friend.name.encode('utf-8'),
                        friend.steam_id)

            # Accept friend invitations
            if friend.relationship == EFriendRelationship.RequestRecipient:
                logger.info("User %s (%d) added me to his/her friends",
                            friend.name,
                            friend.steam_id)
                self.friends.add(friend.steam_id)


    @staticmethod
    def on_friend_added(self, msg):
        """Informs about new friends being added, or shows any errors.
        """
        if msg.body.eresult != 1:
            logger.error("Error adding friend %s (%d)",
                         msg.body.persona_name_added,
                         msg.body.steam_id_added
            )
            logger.error("Eresult: %d", msg.body.eresult)
        else:
            logger.info("%s (%d) is now a friend",
                        msg.body.persona_name_added,
                        msg.body.steam_id_added)


    def on_chat_invite(self, msg):
        """Logs the invite and joins the chat we were invited to.
        """
        logger.info("Invited to %s by %s (%s)", msg.body.chat_name,
                    self.get_name_from_steamid(
                        msg.body.steam_id_patron),
                    msg.body.steam_id_patron)

        self.groups.add_group(msg.body.steam_id_chat, msg.body.chat_name)

        self.join_chat(msg.body.steam_id_chat)


    def on_chat_message(self, msg):
        if msg.body.chat_entry_type == EChatEntryType.Typing:
            logger.info("%s started typing a message to me",
                        self.get_name_from_steamid(msg.body.steamid_from))

        if msg.body.chat_entry_type == EChatEntryType.ChatMsg:
            logger.info("Message from {}: {}".format(
                self.get_name_from_steamid(msg.body.steamid_from).encode('utf-8'),
                msg.body.message.strip().strip('\x00')))

            # Do not interact with ignored users - just log what they're
            # sending
            if msg.body.steamid_from not in config["IGNORED_USERS"]:
                for plugin in self.bot.plugins:
                    plugin.private_chat_hook(msg.body.steamid_from,
                    msg.body.message.decode("utf-8").strip().strip('\x00'))


    def on_group_chat_msg(self, msg):
        groupname = str(self.groups.get_name(msg.body.steamIdChatRoom))

        # Do not interact with ignored users - don't log either
        if msg.body.steamIdChatter not in config["IGNORED_USERS"]:
            logger.info("(Chatroom: {}) {}: {}".format(
                groupname,
                self.get_name_from_steamid(msg.body.steamIdChatter).encode('utf-8').strip(),
                msg.body.text.strip().strip('\x00')))

            for plugin in self.bot.plugins:
                plugin.group_chat_hook(
                    msg.body.steamIdChatRoom,
                    msg.body.steamIdChatter,
                    msg.body.text.decode("utf-8").strip().strip('\x00'))


    def on_chat_member_info(self, msg):
        to_log = ""
        if msg.body.chatAction == 0x01:
            to_log = "({}) {} ({}) entered the chat."
            self.chats[msg.body.steamIdChat].append(msg.body.steamIdUserActedOn)
            for plugin in self.bot.plugins:
                plugin.user_entered_hook(
                    msg.body.steamIdChat,
                    msg.body.steamIdUserActedOn
                )
        elif msg.body.chatAction == 0x02:
            to_log = "({}) {} ({}) left the chat."
            self.chats[msg.body.steamIdChat].remove(msg.body.steamIdUserActedOn)
            for plugin in self.bot.plugins:
                plugin.user_left_hook(
                    msg.body.steamIdChat,
                    msg.body.steamIdUserActedOn
                )
        elif msg.body.chatAction == 0x04:
            to_log = "({}) {} ({}) disconnected."
            self.chats[msg.body.steamIdChat].remove(msg.body.steamIdUserActedOn)
            for plugin in self.bot.plugins:
                plugin.user_left_hook(
                    msg.body.steamIdChat,
                    msg.body.steamIdUserActedOn
                )

        to_log = to_log.format(
            msg.body.steamIdChat,
            self.get_name_from_steamid(msg.body.steamIdUserActedOn).encode('utf-8').strip(),
            msg.body.steamIdUserActedOn)

        logger.info(to_log)


    def on_chat_enter(self, msg):

        if msg.body.enterResponse != 1:
            logger.info("Could not join chat {}({})".format(
                msg.body.chatRoomName,
                msg.body.steamIdChat))
            return

        logger.info("Entered group chat: {}({})".format(
            msg.body.chatRoomName,
            msg.body.steamIdChat))
        self.chats[msg.body.steamIdChat] = []

        for member in msg.body.memberList:
            suser = self.client.get_user(member['steamid'])
            self.chats[msg.body.steamIdChat].append(
                suser
            )

            if self.permissions.get(member['steamid']) is None:
                self.permissions[member['steamid']] = [(msg.body.steamIdChat,
                                                       member['permissions'])]
            else:
                self.permissions[member['steamid']].append(
                    (msg.body.steamIdChat, member['permissions'])
                )

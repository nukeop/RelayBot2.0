import steam.client
import steam.client.builtins.friends

from steam.core.msg import MsgProto
from steam.enums import EResult, EPersonaState, EFriendRelationship
from steam.enums import EChatEntryType
from steam.enums.emsg import EMsg

import logging
import os
import time

import config
import relaybot
logger = logging.getLogger(__name__)


class User(object):
    """Handles interaction with Steam, including logging in and reacting to
    events sent from Steam servers.
    """

    def __init__(self, bot, client):
        logger.info("Creating a User instance")

        self.client = client
        self.client.set_credential_location(os.getcwd())

        self.friends = steam.client.builtins.friends.SteamFriendlist(
            self.client)

        self.bot = bot

        self.client.on('error', self.handle_errors)
        self.client.on('auth_code_required', self.auth_code_prompt)
        self.client.on(EMsg.ClientFriendMsgIncoming, self.on_chat_message)
        self.client.on(EMsg.ClientAccountInfo, self.on_account_info)
        self.client.on(EMsg.ClientFriendsList, self.on_client_friends_list)
        self.client.on(EMsg.ClientAddFriendResponse, self.on_friend_added)
        self.client.on(EMsg.ClientChatInvite, self.on_chat_invite)

        if self.client.relogin_available:
            self.client.relogin()
        else:
            self.client.login(config.STEAM_USER, config.STEAM_PWD)

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
        suser = self.client.get_user(steamid, False)
        return suser.name


    def join_chat(self, chatroomid):
        logger.error("Joining group chats is not implemented yet")


    def send_msg(self, steamid, msg):
        """Sends a message to a steam user.
        """
        sendmsg = MsgProto(EMsg.ClientFriendMsg)
        sendmsg.body.steamid = steamid
        sendmsg.body.chat_entry_type = 1
        sendmsg.body.message = msg
        sendmsg.body.rtime32_server_timestamp = int(time.time())

        self.client.send(sendmsg)

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
            self.client.login(config.STEAM_USER, config.STEAM_PWD, two_factor_code=code)
        else:
            code = raw_input("Enter Steam Guard code: ")
            self.client.login(config.STEAM_USER, config.STEAM_PWD, auth_code=code)


    def on_account_info(self, msg):
        """Sets status to online right after we log in and get our account
        info.
        """
        if msg is None:
            return

        logger.info("Received ClientAccountInfo")
        self.change_status(EPersonaState.Online, config.STEAM_PROFILE_NAME)

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

        self.join_chat(msg.body.steam_id_chat)

    def on_chat_message(self, msg):
        if msg.body.chat_entry_type == EChatEntryType.Typing:
            logger.info("%s started typing a message to me",
                        self.get_name_from_steamid(msg.body.steamid_from))

        if msg.body.chat_entry_type == EChatEntryType.ChatMsg:
            logger.info("Message from %s: %s",
                        self.get_name_from_steamid(msg.body.steamid_from),
                        msg.body.message)

            for plugin in self.bot.plugins:
                plugin.private_chat_hook(msg.body.steamid_from,
                msg.body.message)

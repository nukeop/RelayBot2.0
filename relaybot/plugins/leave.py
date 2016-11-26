import plugin
from config import config

class LeavePlugin(plugin.Plugin):
    """Enables a command that makes the bot leave the chatroom
    """
    def __init__(self, bot):
        super(LeavePlugin, self).__init__(bot)
        self.command = "!leave"


    @property
    def description(self):
        return "Makes me leave a group chat."


    @property
    def long_desc(self):
        return ("When used in a group chat by an admin user, it will make the"
                " bot leave. When used in a private chat, also by an admin"
                " user, it can be used with a group id to make the bot leave a"
                " particular group chat. Commands from non-admin users are"
                " ignored.")


    @property
    def commands(self):
        return {
            "!leave": "makes the bot leave the group chat"
        }


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):

            if not steamid in config["AUTHORIZED_USERS"]:
                self.bot.user.send_msg(steamid, "Unauthorized user. Access"
                                       " denied.")
                return

            groupid = message.split()[1]
            try:
                self.bot.user.leave_chat(int(groupid))
            except ValueError:
                self.bot.user.send_msg(steamid, "Invalid group id.")


    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            #ignore command if issued by a non-admin or regular member
            if not (userid in config["AUTHORIZED_USERS"] or
                    self.has_authority(userid, groupid)):
                return

            self.bot.user.leave_chat(groupid)


    def has_authority(self, userid, groupid):
        """Checks if the user has a rank higher than Member in a given group
        """
        permissions = [x for x in self.bot.user.permissions[userid] if x[0] ==
                       groupid][0][1]
        return (permissions & 3) != 0 #3 bit flag represents owner or officer`

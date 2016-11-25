import plugin

from relaybot import VERSION

class Version(plugin.Plugin):
    """Shows current version of the program to users.
    """
    def __init__(self, bot):
        super(Version, self).__init__(bot)
        self.command = "!version"


    @property
    def description(self):
        return "Shows version and last introduced changes."


    @property
    def long_desc(self):
        return ("!version will show the major and minor versions as well as"
                " the last line added to the changelog.")

    @property
    def commands(self):
        return {
            "!version": "shows program version and the latest changelog entry"
        }


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            self.bot.user.send_msg(steamid, self.get_version())


    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command):
            self.bot.user.send_group_msg(groupid, self.get_version())


    @staticmethod
    def get_version():
        versionstr = "RelayBot v{}.{}".format(VERSION[0], VERSION[1])
        with open('relaybot/changelog.md', 'r') as cl:
            lines = cl.readlines()
            versionstr += '\n'
            versionstr += lines[-1]
        return versionstr

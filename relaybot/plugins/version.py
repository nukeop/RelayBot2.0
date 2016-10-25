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


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            versionstr = "{}.{}".format(VERSION[0], VERSION[1])
            with open('relaybot/changelog.md', 'r') as cl:
                lines = cl.readlines()
                versionstr += '\n'
                versionstr += lines[-1]

            self.bot.user.send_msg(steamid, versionstr)

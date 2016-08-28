import plugin

class Help(plugin.Plugin):
    """Shows info about installed plugins to users.
    """
    def __init__(self, bot):
        super(Help, self).__init__(bot)
        self.command = "!help"

    @property
    def description(self):
        return "See a list of available commands and detailed info about them."

    @property
    def long_desc(self):
        return ("!help - shows a list of all available plugins and what they"
        " do.\n !help <command> - shows detailed information about a command.")

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):
            args = message[:-1].split()
            if len(args) > 1:
                self.bot.user.send_msg(steamid, self.get_long_desc(args[1]))
            else:
                self.bot.user.send_msg(steamid, self.build_help_list())

    def build_help_list(self):
        """Builds a list of short descriptions of plugins along with their
        names.
        """
        result = "\n"
        for plugin in self.bot.plugins:
            result += "{}\n\t{}\n".format(type(plugin).__name__,
                                        plugin.description)
        return result

    def get_long_desc(self, name):
        """Looks for a plugin and gets its long description.
        """
        result = None
        for plugin in self.bot.plugins:
            if type(plugin).__name__ == name:
                result = plugin.long_desc
                break

        if result is not None:
            result = "\nHelp text for {}:\n{}".format(name, result)
        else:
            result = "No such plugin could be found."
        return result

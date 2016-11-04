import plugin

class Help(plugin.Plugin):
    """Shows info about installed plugins to users.
    """
    def __init__(self, bot):
        super(Help, self).__init__(bot)
        self.command_help = "!help"
        self.command_plugins = "!plugins"

    @property
    def description(self):
        return "See a list of available commands and detailed info about them."

    @property
    def long_desc(self):
        return ("!help - shows a list of all available commands and what they"
        " do.\n!plugins <command/plugin name> - shows detailed information about"
        "a plugin.\n!plugins - show a list of all plugins and their"
        " descriptions.")

    @property
    def commands(self):
        return {
            "!help": "shows a list of commands",
            "!plugins": "shows a list of all plugins and their descriptions,"
            " or detailed info about a specific plugin"
        }

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command_help):
            self.bot.user.send_msg(steamid, self.build_help_list())
        elif message.startswith(self.command_plugins):
            args = message[:-1].split()
            if len(args) > 1:
                self.bot.user.send_msg(steamid, self.get_long_desc(args[1]))
            else:
                self.bot.user.send_msg(steamid, self.build_plugin_list())

    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.command_help):
            self.bot.user.send_group_msg(groupid, self.build_help_list())

    def build_help_list(self):
        """Builds a list of commands along with their descriptions.
        """
        result = "\n"
        for plugin in self.bot.plugins:
            if plugin.commands is not None:
                for k, v in plugin.commands.iteritems():
                    result += "{} - {}\n".format(k, v)
        return result

    def build_plugin_list(self):
        """Builds a list of all plugins and their descriptions.
        """
        result = "\n"
        for plugin in self.bot.plugins:
            result += type(plugin).__name__
            result += "\n\t" + plugin.description + "\n"
        return result

    def get_long_desc(self, name):
        """Looks for a plugin and gets its long description.
        """
        plugin_name = None
        result = None
        for _plugin in self.bot.plugins:
            if type(_plugin).__name__.lower() == name.lower():
                plugin_name = type(_plugin).__name__
                result = _plugin.long_desc
                break

        if result is not None:
            result = "\nHelp text for {}:\n{}".format(plugin_name,
                                                      result)
        else:
            result = "No such plugin could be found."
        return result

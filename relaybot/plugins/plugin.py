class Plugin(object):
    """Plugin template - all plugins must inherit from this
    """
    def __init__(self, bot):
        """Constructor. Receives a reference to the bot so that the plugins are
        able to call its various functions. All plugins need to call this
        constructor.
        """
        self.bot = bot

    @property
    def description(self):
        """Description of this plugin's functionality - will be shown to users
        who ask for a list of plugins.
        """
        return ""

    @property
    def long_desc(self):
        """Long description of this plugin's functionality - should be
        exhaustive and describe all nuances of using it. This will be shown to
        users who request help about this particular plugin, which means it should
        be as long as needed.
        """
        return ""

    @property
    def commands(self):
        """Dictionary of commands this plugin reacts to when they're sent to the
        chat, or None if it does not react to commands. This will be displayed
        by the help command to users who request a list of possible commands.
        The keys are available commands and corresponding values are short
        descriptions of what the commands do.
        """
        return None

    def init_hook(self):
        """This will be registered and called exactly once when the bot
        initializes itself.
        """
        pass

    def private_chat_hook(self, steamid, message):
        """This will be registered and called whenever the bot receives a
        private message. It will receive the user's steamid and the sent
        message, in the future possibly also other arguments.
        """
        pass

    def group_chat_hook(self, groupid, userid, message):
        """This will be registered and called whenever anyone sends a message
        to a groupchat the bit is in.
        It will receive the group id, the user's steamid and the sent message,
        in the future possibly also other arguments.
        """
        pass

    def enter_group_chat_hook(self, groupid):
        """This will be registered and called whenever the bot enters a group
        chat. It will receive the group id.
        """
        pass

    def user_entered_hook(self, groupid, userid):
        """Called whenever a user enters a group chat the bot is in.
        """
        pass

    def user_left_hook(self, groupid, userid):
        """Called whenever a user leaves a group chat the bot is in.
        """
        pass

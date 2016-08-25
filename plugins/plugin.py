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
        raise NotImplementedError("Plugin should never be created directly")

    @property
    def long_desc(self):
        """Long description of this plugin's functionality - should be
        exhaustive and describe all nuances of using it. This will be shown to
        users who request help about this particular plugin, which means it should
        be as long as needed.
        """
        raise NotImplementedError("Plugin should never be created directly")

    def init_hook(self):
        """This will be registered and called exactly once when the bot
        initializes itself.
        """
        raise NotImplementedError("Plugin should never be created directly")

    def private_chat_hook(self, steamid, message):
        """This will be registered and called whenever the bot receives a
        private message. It will receive the user's steamid and the sent
        message, in the future possibly also other arguments.
        """
        raise NotImplementedError("Plugin should never be created directly")

    def group_chat_hook(self, groupid, userid, message):
        """This will be registered and called whenever anyone sends a message
        to a groupchat the bit is in.
        It will receive the group id, the user's steamid and the sent message,
        in the future possibly also other arguments.
        """
        raise NotImplementedError("Plugin should never be created directly")

    def enter_group_chat_hook(self, groupid):
        """This will be registered and called whenever the bot enters a group
        chat. It will receive the group id.
        """
        raise NotImplementedError("Plugin should never be created directly")

import json
import logging

import config
import plugin

logger = logging.getLogger(__name__)

class AdminPlugin(plugin.Plugin):
    """Admin panel plugin that allows authorized users to perform various
    administrative functions.
    """
    def __init__(self, bot):
        super(AdminPlugin, self).__init__(bot)
        self.command = "!admin"

    @property
    def description(self):
        return ("Allows authorized users to perform administrative"
                " functions.")

    @property
    def long_desc(self):
        desc = ""
        for k, v in self.commands.iteritems():
            desc += "{} - {}\n".format(k, v)
        return desc

    @property
    def commands(self):
        return {
            "!admin ignore <id>": "adds a user to the list of ignored"
            " users in config",
            "!admin authorize <id>": "adds a user to the list of"
            " authorized users in config",
            "!admin unignore <id>": "removes a user from the list of ignored"
            " users in the config",
            "!admin unauthorize <id>": "removes a user from the list of"
            " authorized users in the config",
            "!admin list": "show authorized and ignored users",
            "!admin eval": "evaluate a python expression - dangerous",
        }

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):

            if not steamid in config.config["AUTHORIZED_USERS"]:
                self.bot.user.send_msg(steamid, "Unauthorized user. Access"
                                       " denied.")
                return

            args = message.split()
            if len(args) > 1:
                if args[1] == "ignore":
                    try:
                        config.add_to(int(args[2]), "IGNORED_USERS")
                        self.bot.user.send_msg(steamid, "User {}"
                                               " ignored.".format(args[2]))
                    except ValueError:
                        config.bot.user.send_msg(steamid, "Invalid Steam id.")
                elif args[1] == "authorize":
                    try:
                        config.add_to(int(args[2]), "AUTHORIZED_USERS")
                        self.bot.user.send_msg(steamid, "User {}"
                                               " authorized.".format(args[2]))
                    except ValueError:
                        self.bot.user.send_msg(steamid, "Invalid Steam id.")
                elif args[1] == "unignore":
                    try:
                        config.remove_from(int(args[2]), "IGNORED_USERS")
                        self.bot.user.send_msg(
                            steamid,
                            "User {} removed from ignore list.".format(args[2])
                        )
                    except ValueError:
                        logger.error("Steam ID {} not found on ignore"
                                     " list.".format(args[2]))
                        self.bot.user.send_msg(steamid, "ID {} not found on"
                                               " ignore list.".format(args[2]))
                elif args[1] == "unauthorize":
                    try:
                        config.remove_from(int(args[2]), "AUTHORIZED_USERS")
                        self.bot.user.send_msg(
                            steamid,
                            "User {} removed from authorized"
                            " list.".format(args[2])
                        )
                    except ValueError:
                        logger.error("Steam ID {} not found on authorized"
                                     " list.".format(args[2]))
                        self.bot.user.send_msg(
                            steamid,
                            "ID {} not found on authorized"
                            " list.".format(args[2])
                        )
                elif args[1] == "list":
                    self.bot.user.send_msg(steamid, "Authorized:\n" +
                                           self.list_from("AUTHORIZED_USERS") +
                                           "\nIgnored:\n" +
                                           self.list_from("IGNORED_USERS"))
                elif args[1] == "eval":
                    try:
                        result = eval(' '.join(args[2:]))
                        self.bot.user.send_msg(steamid, str(result))
                    except Exception as e:
                        self.bot.user.send_msg(steamid, "Command triggered an exception: \n{}".format(str(e)))


    def list_from(self, key):
        msg = '\n'.join(["{}"
                         " ({})".format(self.bot.user.get_name_from_steamid(x),
                                        x) for x in config.config[key]])
        if msg == []:
            return ""
        return msg

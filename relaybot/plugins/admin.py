import json
import logging
import os

from config import config, config_path
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
        }

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.command):

            if not steamid in config["AUTHORIZED_USERS"]:
                self.bot.user.send_msg(steamid, "Unauthorized user. Access"
                                       " denied.")
                return

            args = message[:-1].split()
            if len(args) > 1:
                if args[1] == "ignore":
                    try:
                        self.add_to(int(args[2]), "IGNORED_USERS")
                        self.bot.user.send_msg(steamid, "User {}"
                                               " ignored.".format(args[2]))
                    except:
                        self.bot.user.send_msg(steamid, "Invalid Steam id.")
                elif args[1] == "authorize":
                    try:
                        self.add_to(int(args[2]), "AUTHORIZED_USERS")
                        self.bot.user.send_msg(steamid, "User {}"
                                               " authorized.".format(args[2]))
                    except:
                        self.bot.user.send_msg(steamid, "Invalid Steam id.")
                elif args[1] == "unignore":
                    try:
                        self.remove_from(int(args[2]), "IGNORED_USERS")
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
                        self.remove_from(int(args[2]), "AUTHORIZED_USERS")
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


    def add_to(self, steamid, key):
        config[key].append(steamid)
        self.save_config()


    def remove_from(self, steamid, key):
        config[key].remove(steamid)
        self.save_config()

    def list_from(self, key):
        msg = '\n'.join(["{}"
                         " ({})".format(self.bot.user.get_name_from_steamid(x),
                                        x) for x in config[key]])
        if msg == []:
            return ""
        return msg


    def save_config(self):
        configstr = json.dumps(config, indent=4, sort_keys=True)
        with open(config_path, 'w') as config_file:
            config_file.write(configstr)

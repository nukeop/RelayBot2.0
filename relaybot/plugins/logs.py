import logging
import os
import string

import plugin
logger = logging.getLogger(__name__)


class Logs(plugin.Plugin):
    """Handles saving logs from conversations to separate files.
    """
    def __init__(self, bot):
        super(Logs, self).__init__(bot)
        self.loggers = {}
        self.logs_path = os.path.join(os.getcwd(), "logs")
        self.friend_logs_path = os.path.join(self.logs_path, "friends")
        self.group_logs_path = os.path.join(self.logs_path, "groups")

        try:
            os.makedirs(self.friend_logs_path)
        except:
            logger.error("Could not create {}".format(self.friend_logs_path))

        try:
            os.makedirs(self.group_logs_path)
        except:
            logger.error("Could not create {}".format(self.group_logs_path))


    @property
    def description(self):
        return "Handles saving chat logs to separate files."


    @property
    def long_desc(self):
        return ("Creates a directory for logs, separating group chats and"
                " private chats. Every conversation will be saved and/or"
                " appended to a separate log, one for every user and/or"
                " group.")


    def private_chat_hook(self, steamid, message):
        if self.loggers.get(steamid) is None:
            self.setup_logger(steamid, friend=True)
        self.loggers[steamid].info("({}) {}: {}".format(
            steamid,
            self.bot.user.get_name_from_steamid(steamid),
            message
        ))


    def group_chat_hook(self, groupid, userid, message):
        if self.loggers.get(groupid) is None:
            self.setup_logger(groupid)
        self.loggers[groupid].info("[({}) {}]({}) {}: {}".format(
            groupid,
            self.bot.user.groups.get_name(groupid),
            userid,
            self.bot.user.get_name_from_steamid(userid).encode('utf-8'),
            message
        ))


    def make_filename(self, name, steamid):
        filename = "{}_{}.log".format(
            steamid,
            ''.join([c for c in list(name) if c in string.ascii_letters or c in
                     string.digits])
        )
        return filename


    def setup_logger(self, steamid, friend=False):
        name = (
            self.make_filename(
                self.bot.user.get_name_from_steamid(steamid),
                steamid
            ) if friend else
            self.make_filename(
                self.bot.user.groups.get_name(steamid),
                steamid
            )
        )
        self.loggers[steamid] = logging.getLogger(__name__+'.'+str(steamid))
        self.loggers[steamid].setLevel(logging.DEBUG)
        self.loggers[steamid].propagate = False
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        filename = (os.path.join(self.friend_logs_path, name) if friend else
        os.path.join(self.group_logs_path, name))
        handler = logging.FileHandler(filename)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        self.loggers[steamid].addHandler(handler)

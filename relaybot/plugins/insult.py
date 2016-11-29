import logging
import random

import plugin

logger = logging.getLogger(__name__)

class Insult(plugin.Plugin):
    def __init__(self, bot):
        super(Insult, self).__init__(bot)
        self.use_command = "!insult"
        self.add_command = "!addinsult"
        self.init_db()


    def commands(self):
        return {
            "!insult": "",
            "!addinsult": ""
        }


    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.use_command):
            self.bot.user.send_group_msg(groupid, self.format_insult(groupid, message))
        elif message.startswith(self.add_command):
            self.bot.user.send_group_msg(groupid, self.add_insult(userid, message))


    def format_insult(self, groupid, message):
        username = ' '.join(message.split()[1:])
        steamid = self.bot.user.username_to_steamid(groupid, username)

        if not steamid:
            return "Unknown user {}.".format(username)

        return self.get_insult().format(username)


    def get_insult(self):
        rows = self.bot.database.select("insults", "*")
        if len(rows)<1:
            return "No insults in the database."
        else:
            row = random.choice(rows)

            return row[1]


    def add_insult(self, steamid, message):
        tokens = message.split()
        if len(tokens)<2:
            return "No content. Insult not added."

        self.bot.database.insert("insults", "content, author", "?, ?",
                                (
                                    ' '.join(tokens[1:]),
                                    self.bot.user.get_name_from_steamid(steamid)
                                )
        )
        return "Insult added."


    def init_db(self):
        tables = self.bot.database.select("sqlite_master", "name",
                                         "type='table'")

        for table in tables:
            if table[0] == "insults":
                return

        logger.info("Creating insults table in the database")
        self.bot.database.create_table("insults",
                                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                       "content TEXT NOT NULL,"
                                       "author TEXT NOT NULL"
        )

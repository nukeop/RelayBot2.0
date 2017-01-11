# -*- coding: utf-8 -*-
import logging
import random

import plugin

logger = logging.getLogger(__name__)


class Trivia(plugin.Plugin):
    """Plugin that works similarly to the joke plugin, but it handles trivia
    instead. Theoretically this could be abstracted and combined with jokes,
    but in the future we will probably want it to be handled differently, so it
    should stay as a separate module.
    """
    def __init__(self, bot):
        super(Trivia, self).__init__(bot)
        self.use_command = "!trivia"
        self.add_command = "!addtrivia"

        self.init_db()


    @property
    def description(self):
        return "Shows trivia added by users."


    @property
    def long_desc(self):
        return ""


    @property
    def commands(self):
        return {
            "!trivia": "shows random trivia",
            "!addtrivia": "adds a new piece of trivia to the database"
        }


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.use_command):
            self.bot.user.send_msg(steamid, self.get_trivia())
        elif message.startswith(self.add_command):
            self.bot.user.send_msg(steamid, self.add_trivia(steamid, message))


    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.use_command):
            self.bot.user.send_group_msg(groupid, self.get_trivia())
        elif message.startswith(self.add_command):
            self.bot.user.send_group_msg(groupid, self.add_trivia(userid, message))


    def get_trivia(self):
        rows = self.bot.database.select("trivia", "*")
        if len(rows)<1:
            return "No trivia in the database."
        else:
            row = random.choice(rows)

            return ("User {} shared the following piece of"
                    " trivia:\n\n{}".format(row[2], row[1]).encode('utf-8'))


    def add_trivia(self, steamid, message):
        tokens = message.split()
        if len(tokens)<2:
            return "No content. Trivia not added."
        else:
            self.bot.database.insert("trivia", "content, author", "?, ?",
                            (
                                ' '.join(tokens[1:]),
                                self.bot.user.get_name_from_steamid(steamid)
                            )
            )
            return "Trivia added."


    def init_db(self):
        tables = self.bot.database.select("sqlite_master", "name",
                                          "type='table'")
        for table in tables:
            if table[0] == "trivia":
                return

        logger.info("Creating trivia table in the database")
        self.bot.database.create_table("trivia",
                                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                       "content TEXT NOT NULL,"
                                       "author TEXT NOT NULL"
        )

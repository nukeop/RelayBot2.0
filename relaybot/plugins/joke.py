# -*- coding: utf-8 -*-
import logging
import random

import plugin
import util

logger = logging.getLogger(__name__)

class Joke(plugin.Plugin):
    """Plugin allowing users to add new jokes to the database, display ones
    stored in it, and rate the ones they see.

    Individual jokes as stored in the database have an id, the content, and an
    author. The author needs to be stored with the author to display the joke
    along with the person who added it. Ratings are stored in a separate table.
    """
    def __init__(self, bot):
        super(Joke, self).__init__(bot)
        self.use_command = "!joke"
        self.add_command = "!addjoke"
        self.rate_command = "!ratejoke"

        self.init_db()


    @property
    def description(self):
        return "Shows jokes and lets you add them and rate them."


    @property
    def long_desc(self):
        return ("!joke - shows a random joke.\n!addjoke <text> - adds a new"
                " joke to the database.\n!ratejoke <id> <rating (0-5)> -"
                "lets you rate a joke.")

    @property
    def commands(self):
        return {
            "!joke": "shows a random joke",
            "!addjoke": "adds a new joke to the database",
            "!ratejoke <id> <score>": "rates a joke from 0 to 5 stars"
        }

    def get_joke(self):
        rows = self.bot.database.select("jokes", "*")
        if len(rows)<1:
            return "No jokes in the database."
        else:
            row = random.choice(rows)

            ratings = [int(x[0]) for x in self.bot.database.select(
                "jokes_ratings",
                "rating",
                "jokeid={}".format(row[0])
            )]

            rating = 0
            if len(ratings) > 0:
                rating = sum(ratings)/float(len(ratings))
            rating = util.rating_to_stars(rating)

            return ("Joke #{} by {} ({}):\n"
            "{}".format(row[0], row[2].encode('utf-8'), rating,
                        row[1].encode('utf-8')))

    def add_joke(self, steamid, message):
        tokens = message.split()
        if len(tokens)<2:
            return "No content. Joke not added."
        else:
            self.bot.database.insert("jokes", "content, author", "?, ?",
                        (
                            " ".join(tokens[1:]),
                            self.bot.user.get_name_from_steamid(steamid)
                        )
            )
            return "Joke added."

    def rate_joke(self, steamid, message):
        tokens = message.split()
        if len(tokens)!=3:
            return ("Incorrect number of arguments. You have to supply"
                    " the id of the joke you want to rate, and a rating.")
        else:
            if int(tokens[2])>5 or int(tokens[2])<0:
                return ("Rating must be between 0 and 5.")

            row = self.bot.database.select("jokes", "*",
                                            "id={}".format(tokens[1]))
            if len(row)<1:
                return

            self.bot.database.insert(
                "jokes_ratings",
                "jokeid, rating",
                "?, ?",
                (tokens[1], tokens[2])
            )

            return "Joke rated."

    def private_chat_hook(self, steamid, message):
        if message.startswith(self.use_command):
            self.bot.user.send_msg(steamid, self.get_joke())
        elif message.startswith(self.add_command):
            self.bot.user.send_msg(steamid, self.add_joke(steamid, message))
        elif message.startswith(self.rate_command):
            self.bot.user.send_msg(steamid, self.rate_joke(steamid, message))

    def group_chat_hook(self, groupid, userid, message):
        if message.startswith(self.use_command):
            self.bot.user.send_group_msg(groupid, self.get_joke())
        elif message.startswith(self.add_command):
            self.bot.user.send_group_msg(groupid, self.add_joke(userid, message))
        elif message.startswith(self.rate_command):
            self.bot.user.send_group_msg(groupid, self.rate_joke(userid, message))

    def init_db(self):
        tables = self.bot.database.select("sqlite_master", "name",
                                         "type='table'")
        jokes_table_exists = False
        ratings_table_exists = False
        for table in tables:
            if table[0] == "jokes":
                jokes_table_exists = True
            elif table[0] == "jokes_ratings":
                ratings_table_exists = True

        if not jokes_table_exists:
            logger.info("Creating jokes table in the database")
            self.bot.database.create_table("jokes",
                                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                    "content TEXT NOT NULL,"
                                    "author TEXT NOT NULL"
            )

        if not ratings_table_exists:
            logger.info("Creating ratings table in the database")
            self.bot.database.create_table("jokes_ratings",
                                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                           "jokeid INTEGER,"
                                           "rating INTEGER CHECK(rating >=0 AND"
                                           " rating <6),"
                                           "FOREIGN KEY(jokeid) REFERENCES"
                                           " jokes(id)"
            )


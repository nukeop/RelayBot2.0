import logging
import random

import database
import plugin

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


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.use_command):
            rows = self.bot.database.select("jokes", "*")
            if len(rows)<1:
                self.bot.user.send_msg(steamid, "No jokes in the database.")
            else:
                row = random.choice(rows)
                self.bot.user.send_msg(steamid, "Joke #{} by {}:\n"
                                       "{}".format(row[0], row[2], row[1]))
        elif message.startswith(self.add_command):
            tokens = message.split()
            if len(tokens)<2:
                self.bot.user.send_msg(steamid, "No content. Joke not added.")
            else:
                self.bot.database.insert("jokes", "content, author", "?, ?",
                                         (
                                             " ".join(tokens[1:]),
                                             self.bot.user.get_name_from_steamid(steamid)
                                         )
                )
                self.bot.user.send_msg(steamid, "Joke added.")
        elif message.startswith(self.rate_command):
            tokens = message.split()
            if len(tokens)!=3:
                self.bot.user.send_msg(steamid, "Incorrect number of"
                                       " arguments. You have to supply the"
                                       " id of the joke you want to rate,"
                                       " and a rating.")
            else:
                self.bot.user.send_msg(steamid, "Rate command used")

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

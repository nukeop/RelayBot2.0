import logging

import plugin

logger = logging.getLogger(__name__)

class Note(plugin.Plugin):
    """Plugin that lets users save short notes and display them later.
    Modification is not allowed, however the notes can be deleted and re-added.
    """
    def __init__(self, bot):
        super(Note, self).__init__(bot)
        self.use_command = "!shownote"
        self.add_command = "!addnote"

        self.init_db()


    @property
    def description(self):
        return "Lets you save and display short notes."


    @property
    def long_desc(self):
        return self.description


    @property
    def commands(self):
        return {
            "!shownote": "shows your notes",
            "!addnote": "adds a new note"
        }


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.use_command):
            self.bot.user.send_msg(steamid, self.get_all_notes(steamid))
        elif message.startswith(self.add_command):
            self.bot.user.send_msg(steamid, self.add_note(steamid, message))


    def get_all_notes(self, steamid):
        records = self.bot.database.select("notes", "id, content",
                                           "author='{}'".format(steamid))
        if len(records) == 0:
            return "You have no notes."

        records = sorted(records, key=lambda x: x[0])
        allrecords = "Your notes:\n\n"
        for i, r in enumerate(records):
            allrecords += "{}. {}\n".format(i, r[1].encode('utf-8'))
        return allrecords


    def add_note(self, steamid, message):
        tokens = message.split()
        if len(tokens)<2:
            return "No content. Note not added."
        else:
            self.bot.database.insert("notes", "content, author", "?, ?",
                            (
                                ' '.join(tokens[1:]),
                                steamid
                            )
            )
            return "Note added."


    def init_db(self):
        tables = self.bot.database.select("sqlite_master", "name",
                                          "type='table'")
        for table in tables:
            if table[0] == "notes":
                return

        logger.info("Creating notes table in the database")
        self.bot.database.create_table("notes",
                                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                       "content TEXT NOT NULL,"
                                       "author INTEGER NOT NULL"
        )

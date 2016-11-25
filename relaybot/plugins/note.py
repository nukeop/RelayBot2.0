import logging
import sqlite3

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
        self.delete_command = "!deletenote"

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
            "!shownote": "without arguments - shows all your keys, with an"
            "argument - shows a note corresponding to that key",
            "!addnote": "adds a new note",
            "!deletenote": "deletes the note corresponding to given key"
        }


    def private_chat_hook(self, steamid, message):
        if message.startswith(self.use_command) and len(message.split())==1:
            self.bot.user.send_msg(steamid, self.get_all_notes_keys(steamid))
        elif message.startswith(self.use_command):
            self.bot.user.send_msg(steamid, self.get_note(steamid, message))
        elif message.startswith(self.add_command):
            self.bot.user.send_msg(steamid, self.add_note(steamid, message))
        elif message.startswith(self.delete_command):
            self.bot.user.send_msg(steamid, self.delete_note(steamid, message))


    def get_all_notes_keys(self, steamid):
        records = self.bot.database.select("notes", "key",
                                           "author='{}'".format(steamid))
        if len(records) == 0:
            return "You have no notes."

        records = sorted(records, key=lambda x: x[0])
        allrecords = "Your notes:\n\n"
        for i, r in enumerate(records):
            allrecords += "{}. {}\n".format(i+1, r[0].encode('utf-8'))
        return allrecords


    def get_note_record(self, steamid,  message):
        key = message.split()[1]
        records = self.bot.database.select("notes", "content",
                                           "key='{}' AND author='{}'"
                                           .format(key, steamid))
        return records[0] if len(records)>0 else None


    def get_note(self, steamid, message):
        tokens = message.split()
        if len(tokens)<2:
            return "You have to provide the key."

        note = self.get_note_record(steamid, message)
        if note is None:
            return "No note found for key '{}'.".format(tokens[1])

        return str(note[0].encode('utf-8'))


    def add_note(self, steamid, message):
        tokens = message.split()
        if len(tokens)<3:
            return "No content. Note not added."
        else:
            try:
                self.bot.database.insert("notes", "key, content, author", "?, ?, ?",
                                (
                                    tokens[1],
                                    ' '.join(tokens[2:]),
                                    steamid
                                )
                )
                return "Note added."
            except sqlite3.IntegrityError:
                return ("You already made a note with key"
                        " '{}'.".format(tokens[1]))


    def delete_note(self, steamid, message):
        tokens = message.split()
        if len(tokens)<2:
            return "You have to provide the key."

        note = self.get_note_record(steamid, message)
        if note is None:
            return "No note found for key '{}'.".format(tokens[1])

        self.bot.database.delete("notes", "key='{}' AND "
                                 "author='{}'".format(tokens[1], steamid))
        return "Note deleted."


    def init_db(self):
        tables = self.bot.database.select("sqlite_master", "name",
                                          "type='table'")
        for table in tables:
            if table[0] == "notes":
                return

        logger.info("Creating notes table in the database")
        self.bot.database.create_table("notes",
                                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                       "key TEXT UNIQUE NOT NULL,"
                                       "content TEXT NOT NULL,"
                                       "author INTEGER NOT NULL"
        )

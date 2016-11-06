# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

class Groups(object):
    """Translates steam ids to group names, and keeps a table in the database
    for fast lookup.
    """
    def __init__(self, db):
        self.db = db
        self.init_db()

    def add_group(self, steamid, name):
        self.db.insert("groups", "groupid, groupname", "?, ?",
                       (
                           steamid,
                           name
                       )
        )

    def get_name(self, steamid):
        name =\
        self.db.select("groups", "groupname", "groupid='{}'".format(steamid))
        if len(name) > 0:
            name = name[0][0].encode('utf-8').strip()
        else:
            name = str(steamid)
        return name

    def init_db(self):
        tables = self.db.select("sqlite_master", "name",
                                          "type='table'")

        for table in tables:
            if table[0] == "groups":
                return

        logger.info("Creating groups table in the database")
        self.db.create_table("groups",
                             "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                             "groupid INTEGER NOT NULL,"
                             "groupname TEXT NOT NULL"
        )

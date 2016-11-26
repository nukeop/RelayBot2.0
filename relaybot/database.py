import sqlite3

class Database(object):
    """Interface to a local database that stores data for the bot and its
    plugins.
    """
    def __init__(self, dbname):
        self.dbname = dbname

        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()


    def select(self, table, fields, condition=None):
        if condition is not None:
            self.cursor.execute("SELECT {} FROM {} WHERE {}".format(fields, table,
                                                            condition))
        else:
            self.cursor.execute("SELECT {} FROM {}".format(fields, table))

        return self.cursor.fetchall()


    def create_table(self, table, cols):
        query = "CREATE TABLE {}({})".format(table, cols)
        self.cursor.execute(query)
        self.conn.commit()


    def insert(self, table, columns, values, params):
        query = "INSERT INTO {}({}) VALUES ({})".format(table, columns, values)
        self.cursor.execute(query, params)
        self.conn.commit()


    def delete(self, table, condition):
        query = "DELETE FROM {} WHERE {}".format(table, condition)
        self.cursor.execute(query)
        self.conn.commit()

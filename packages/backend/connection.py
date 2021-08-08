import os
import sqlite3

class Query():
    def __init__(self, directory, parent):
        self.directory = directory
        self.database = os.path.join(self.directory, 'Engines.db')
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

    def query(self, query, params=None):
        if params == None:
            return self.cursor.execute(query)
        else:
            return self.cursor.execute(query, (params,))

    def close(self):
        self.cursor.close()

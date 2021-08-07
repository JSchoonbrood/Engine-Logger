import sqlite3
import os
import datetime
from shutil import copy2
from pathlib import Path

class Operations():
    def __init__(self, directory, parent=None):
        self.directory = str(directory)
        self.backups = os.path.join(self.directory, 'Backups')
        self.database = os.path.join(self.directory, 'Engines.db')

    def locate_database(self):
        if os.path.isfile(self.database):
            return True
        else:
            return False

    def backup_database(self):
        Path(self.backups).mkdir(parents=True, exist_ok=True)
        backup_fname = (datetime.datetime.now().strftime("%d-%m-%Y")) + '.db'
        copy2(self.database, os.path.join(self.backups, backup_fname))
        return

    def create_database(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('''
                        CREATE TABLE Engine(id INTEGER PRIMARY KEY,
                                            title TEXT,
                                            engine TEXT,
                                            car TEXT,
                                            customer TEXT)''')

        connection.commit()
        connection.close()
        return

    def get_title(self, job_id):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('''SELECT title FROM Engine WHERE id = ?''', (job_id,)) 

        title = cursor.fetchone()
        title = str(title).strip("'(),")
        return str(title)
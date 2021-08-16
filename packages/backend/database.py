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
                        CREATE TABLE Jobs(job_id INTEGER PRIMARY KEY,
                                            title TEXT,
                                            car TEXT,
                                            engine TEXT,
                                            build_date TEXT,
                                            built_by TEXT,
                                            customer TEXT)''')

        cursor.execute('''
                        CREATE TABLE Block(job_id INTEGER PRIMARY KEY,
                                            make TEXT,
                                            engine_type TEXT,
                                            boresize TEXT,
                                            liner_protrusion TEXT,
                                            main_tunnel_size TEXT,
                                            notes TEXT,
                                            engine_code, TEXT,
                                            number_cylinders TEXT,
                                            firing_order TEXT,
                                            comp_ratio TEXT,
                                            stroke TEXT,
                                            cc TEXT,
                                            FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE Pistons(job_id INTEGER PRIMARY KEY,
                                                piston_make TEXT,
                                                piston_part_number TEXT,
                                                piston_clearance TEXT,
                                                piston_pin_id TEXT,
                                                top_ring_type TEXT,
                                                top_ring_part TEXT,
                                                second_ring_type TEXT,
                                                second_ring_part TEXT,
                                                oil_ring_type TEXT,
                                                oil_ring_part TEXT,
                                                notes TEXT,
                                                FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE PistonData(id INTEGER PRIMARY KEY,
                                                    piston_number INTEGER,
                                                    piston_diameter TEXT,
                                                    piston_weight TEXT,
                                                    top_ring_gap TEXT,
                                                    top_ring_size TEXT,
                                                    top_ring_thickness TEXT,
                                                    second_ring_gap TEXT,
                                                    second_ring_size TEXT,
                                                    second_ring_thickness TEXT,
                                                    oil_ring_gap TEXT,
                                                    oil_ring_size TEXT,
                                                    oil_ring_thickness TEXT,
                                                    wristpin_weight TEXT,
                                                    wristpin_od TEXT,
                                                    job_id INTEGER FOREIGN KEY REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE ConRods(job_id INTEGER PRIMARY KEY,
                                                rod_make TEXT,
                                                rod_bolt_make TEXT,
                                                rod_length TEXT,
                                                notes TEXT,
                                                FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE ConRodData(id INTEGER PRIMARY KEY,
                                                    rod_number INTEGER,
                                                    rod_weight TEXT,
                                                    rod_id TEXT,
                                                    smallend_id TEXT,
                                                    bigend_id TEXT,
                                                    smallend_od TEXT,
                                                    bigend_od TEXT,
                                                    job_id INTEGER
                                                    FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE Balancing(job_id INTEGER PRIMARY KEY,
                                                    pistons_weight TEXT,
                                                    rod_weight TEXT,
                                                    small_end_weight TEXT,
                                                    big_end_weight TEXT,
                                                    wristpin_weight TEXT,
                                                    circlips_weight TEXT,
                                                    small_end_total TEXT,
                                                    big_end_total TEXT,
                                                    notes TEXT,
                                                    FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE Crank(job_id INTEGER PRIMARY KEY,
                                                crank_make TEXT,
                                                crank_part TEXT,
                                                main_journal_size TEXT,
                                                main_bearing_oversize TEXT,
                                                main_bearing_make TEXT,
                                                main_bearing_type TEXT,
                                                main_bearing_thickness TEXT,
                                                main_bearing_clearance TEXT,
                                                crank_endfloat TEXT,
                                                rod_bolt_stretch TEXT,
                                                big_end_journal_size TEXT,
                                                big_end_bearing_oversize TEXT,
                                                big_end_make TEXT,
                                                big_end_bearing_thickness TEXT,
                                                big_end_bearing_clearance TEXT,
                                                notes TEXT,
                                                FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE OilPump(job_id INTEGER PRIMARY KEY,
                                                pump_type TEXT,
                                                part_number TEXT,
                                                pump_clearance TEXT,
                                                end_clearance TEXT,
                                                notes TEXT,
                                                FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE BlockParts()''')

        cursor.execute('''CREATE TABLE ExternalBlockCosts()''')

        cursor.execute('''CREATE TABLE CylinderHead()''')

        cursor.execute('''CREATE TABLE IntakeCam1()''')

        cursor.execute('''CREATE TABLE ExhCam1()''')

        cursor.execute('''CREATE TABLE Carburettor()''')

        connection.commit()
        connection.close()
        return

    def get_title(self, job_id):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('''SELECT title FROM Engine WHERE job_id = ?''', (job_id,)) 

        title = cursor.fetchone()
        title = str(title).strip("'(),")
        return str(title)
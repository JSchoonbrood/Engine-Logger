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

        cursor.execute('''CREATE TABLE BlockData(id INTEGER PRIMARY KEY,
                                                    job_id INTEGER,
                                                    bore_top_measurement TEXT,
                                                    bore_middle_measurement TEXT,
                                                    bore_small_measurement TEXT,
                                                    bore_oval TEXT,
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
                                                    job_id INTEGER,
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
                                                    FOREIGN KEY (job_id) REFERENCES Pistons(job_id))''')

        cursor.execute('''CREATE TABLE ConRods(job_id INTEGER PRIMARY KEY,
                                                rod_make TEXT,
                                                rod_bolt_make TEXT,
                                                rod_length TEXT,
                                                notes TEXT,
                                                FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE ConRodData(id INTEGER PRIMARY KEY,
                                                    job_id INTEGER,
                                                    rod_number INTEGER,
                                                    rod_weight TEXT,
                                                    smallend_id TEXT,
                                                    bigend_id TEXT,
                                                    smallend_od TEXT,
                                                    bigend_od TEXT,  
                                                    FOREIGN KEY (job_id) REFERENCES ConRods(job_id))''')

        cursor.execute('''CREATE TABLE BalancingData(id INTEGER PRIMARY KEY,
                                                    job_id INTEGER,
                                                    piston_number INTEGER,
                                                    pistons_weight TEXT,
                                                    rod_number INTEGER,
                                                    rod_weight TEXT,
                                                    small_end_weight TEXT,
                                                    big_end_weight TEXT,
                                                    wristpin_id INTEGER,
                                                    wristpin_weight TEXT,
                                                    circlips_id INTEGER,
                                                    circlips_weight TEXT,
                                                    small_end_total TEXT,
                                                    big_end_total TEXT,
                                                    bearings_weight TEXT,
                                                    notes TEXT,
                                                    FOREIGN KEY (job_id) REFERENCES Jobs(job_id)
                                                    FOREIGN KEY (piston_number) REFERENCES PistonData(piston_number)
                                                    FOREIGN KEY (rod_number) REFERENCES ConRodData(rod_number))''')

        cursor.execute('''CREATE TABLE Crank(job_id INTEGER PRIMARY KEY,
                                                crank_make TEXT,
                                                crank_part TEXT,
                                                main_journal_size TEXT,
                                                main_bearing_oversize TEXT,
                                                main_bearing_make TEXT,
                                                main_bearing_type TEXT,
                                                crank_endfloat TEXT,
                                                rod_bolt_stretch TEXT,
                                                big_end_journal_size TEXT,
                                                big_end_bearing_oversize TEXT,
                                                big_end_make TEXT,
                                                notes TEXT,
                                                FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        cursor.execute('''CREATE TABLE CrankData(id INTEGER PRIMARY KEY,
                                                    job_id INTEGER,
                                                    journal_type TEXT,
                                                    journal_number INTEGER,
                                                    journal_size TEXT,
                                                    bearing_thickness TEXT,
                                                    bearing_clearance TEXT,
                                                    FOREIGN KEY (job_id) REFERENCES Crank(job_id))''')

        cursor.execute('''CREATE TABLE OilPump(job_id INTEGER PRIMARY KEY,
                                                pump_type TEXT,
                                                part_number TEXT,
                                                pump_clearance TEXT,
                                                end_clearance TEXT,
                                                notes TEXT,
                                                FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')


        cursor.execute('''CREATE TABLE BlockParts(job_id INTEGER PRIMARY KEY,
                                                    block TEXT,
                                                    seal_adapter TEXT,
                                                    primary_fastner TEXT,
                                                    secondary_fastner TEXT,
                                                    freeze_plug TEXT,
                                                    cam_bearing TEXT, 
                                                    head_dowel TEXT,
                                                    bellhousing_dowel TEXT,
                                                    timingcover_dowel TEXT,
                                                    maincap_dowel TEXT,
                                                    oilpump_dowel TEXT,
                                                    head_dowel TEXT,
                                                    rearmainseal_adapter TEXT,
                                                    rearmainseal TEXT,
                                                    mainbearing TEXT,
                                                    rod TEXT,
                                                    piston TEXT,
                                                    rings TEXT,
                                                    oilpump TEXT,
                                                    pickuptube TEXT,
                                                    driverod TEXT,
                                                    oilpump_bolt TEXT,
                                                    oilpan TEXT,
                                                    flywheel TEXT,
                                                    flywheel_bolt TEXT,
                                                    oilpan_gasket TEXT,
                                                    harmonic_balancer TEXT,
                                                    balancedbolt TEXT,
                                                    FOREIGN KEY (job_id) REFERENCES Jobs(job_id))''')

        #cursor.execute('''CREATE TABLE ExternalBlockCosts()''')

        #cursor.execute('''CREATE TABLE CylinderHead()''')

        #cursor.execute('''CREATE TABLE IntakeCam1()''')

        #cursor.execute('''CREATE TABLE ExhCam1()''')

        #cursor.execute('''CREATE TABLE Carburettor()''')

        connection.commit()
        connection.close()
        return
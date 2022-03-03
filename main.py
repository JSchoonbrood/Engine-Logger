"""
@Author: Jake Schoonbrood
@Application: Engine Logger
@Version: V1.000 Beta
@PythonVersion: Python 3.9.6 64Bit
"""

import os
import sys
#import bcrypt

from PySide2 import QtCore, QtGui, QtWidgets
from pathlib import Path
from packages import home
from packages.backend import database
from packages.backend import config
from packages.engines import job_menu
from packages.backend import connection
#from qt_material import apply_stylesheet

# Adds support for MacOS + Windows
if sys.platform == "darwin" or sys.platform == "darwin":
    directory = '/Library/Preferences/JSchoonbrood/EngineLogger/'
elif sys.platform == "win32":
    directory = '%s\\JSchoonbrood\EngineLogger\\' % os.environ['APPDATA']

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setObjectName("window")
        
        self.construct_ui()

    def construct_ui(self):
        self.setMinimumSize(QtCore.QSize(0, 0))
        screens = QtWidgets.QApplication.screens()

        # Obsolete code
        #self.move((resolution.width() / 2) - (self.frameSize().width() / 2),        
        #          (resolution.height() / 2) - (self.frameSize().height() / 2))

        # Detects number of monitors
        if len(screens) == 1:
            # Display on primary monitor
            resolution = QtWidgets.QApplication.primaryScreen().availableGeometry()
            self.setGeometry(resolution)
            self.showMaximized()
        else:
            # Display on secondary monitor
            self.setGeometry(screens[1].availableGeometry())
            self.showMaximized()

        self.setWindowTitle("Engine Logger - Menu")

        # The stack containing all Widgets
        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)
        self.show()

        self.home = home.Widget(directory, self)
        self.home.job_menu_signal.connect(self.switch_to_job_menu)

        self.stack.addWidget(self.home)
        self.stack.setCurrentWidget(self.home)

    @QtCore.Slot(int)
    def switch_to_job_menu(self, job_id):
        self.job_menu = job_menu.Widget(directory, job_id, self)
        self.job_menu.job_id_signal.connect(self.update_title)
        
        self.stack.addWidget(self.job_menu)
        self.stack.setCurrentWidget(self.job_menu)
        new_title = self.get_title(job_id)
        self.setWindowTitle(("Engine Logger - " + new_title))

    @QtCore.Slot()
    def switch_to_home(self):
        self.stack.setCurrentWidget(self.home)
        self.stack.removeWidget(self.checklist)
        self.setWindowTitle("Engine Logger - Menu")

    @QtCore.Slot(str)
    def update_title(self, new_title):
        self.setWindowTitle("Engine Logger - " + new_title)

    def get_title(self, job_id):
        database = connection.Query(directory, self)
        cursor = database.query('''SELECT title FROM Jobs WHERE job_id = ?''', (job_id,))

        title = cursor.fetchone()
        title = str(title).strip("'(),")
        return str(title)


def backend():
    Path(directory).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(directory, 'Manuals')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(directory, 'Gallery')).mkdir(parents=True, exist_ok=True) 
    
    # Backend check to locate / create database
    if not (database.Operations(directory).locate_database()):
        database.Operations(directory).create_database()
    database.Operations(directory).backup_database()

    if not (config.Config(directory).locate_config()):
        config.Config(directory).create_config()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setObjectName("app")
    #apply_stylesheet(app, theme='dark_red.xml')
    

    window = MainWindow(None)

    with open("packages/themes/universal_dark.qss", "r") as f:
        _style = f.read()
        window.setStyleSheet(_style) # Sets external stylesheet to application wide widgets

    #window.show()

    sys.exit(app.exec_()) #PyQt6: exec(), PyQt5: exec_()

if __name__ == '__main__':
    backend()
    main()
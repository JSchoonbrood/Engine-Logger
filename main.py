"""
@Author: Jake Schoonbrood
@Application: Engine Logger
@Version: V1.000
@PythonVersion: Python 3.9.6 64Bit
"""

import os
import sys
import bcrypt

from PySide2 import QtCore, QtGui, QtWidgets
from pathlib import Path
from packages import home
from packages.backend import database
from packages.backend import config
from packages.engines import checklist
from packages.backend import connection
from qt_material import apply_stylesheet

if sys.platform == "darwin" or sys.platform == "darwin":
    directory = '/Library/Preferences/JSchoonbrood/EngineLogger/'
elif sys.platform == "win32":
    directory = '%s\\JSchoonbrood\EngineLogger\\' % os.environ['APPDATA']

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.construct_ui()

    def construct_ui(self):
        resolution = QtWidgets.QDesktopWidget().availableGeometry()
        self.setGeometry(resolution)

        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

        self.showMaximized()

        self.setWindowTitle("Engine Logger - Menu")

        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)
        self.show()

        self.home = home.Widget(directory, self)
        self.home.checklist_signal.connect(self.switch_to_checklist)

        self.stack.addWidget(self.home)
        self.stack.setCurrentWidget(self.home)

    @QtCore.Slot(int)
    def switch_to_checklist(self, job_id):
        self.checklist = checklist.Widget(directory, job_id, self)
        self.checklist.title_signal.connect(self.update_title)
        self.stack.addWidget(self.checklist)
        self.stack.setCurrentWidget(self.checklist)
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
    
    if not (database.Operations(directory).locate_database()):
        database.Operations(directory).create_database()
    database.Operations(directory).backup_database()

    if not (config.Config(directory).locate_config()):
        config.Config(directory).create_config()


def main():
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_red.xml')

    window = MainWindow(None)
    window.show()

    sys.exit(app.exec_()) #PyQt6: exec(), PyQt5: exec_()

if __name__ == '__main__':
    backend()
    main()
import sqlite3
import os
from PySide2 import QtCore, QtGui, QtWidgets
from packages.engines import wizard

class Widget(QtWidgets.QWidget):
    def __init__(self, directory, job_id, parent):
        super(Widget, self).__init__()
        self.directory = str(directory)
        self.database = os.path.join(self.directory, 'Engines.db')
        self.job_id = job_id
        self.constrct_ui()
        #self.read_database()

#    def read_database(self):

    def constrct_ui(self):
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")

        self.menu = QtWidgets.QComboBox()

        self.block_label = QtWidgets.QLabel("Engine Block")

        self.head_label = QtWidgets.QLabel("Cylinderhead")

        self.ancillaries_label = QtWidgets.QLabel("Ancillaries")

        self.electrical_label = QtWidgets.QLabel("Electrical")

        self.notes_label = QtWidgets.QLabel("Notes")

  #  def populate_menu(self):
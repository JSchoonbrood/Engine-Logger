from PySide2 import QtCore, QtGui, QtWidgets
from packages.backend import connection

title_font = QtGui.QFont()
title_font.setPointSize(18)

main_font = QtGui.QFont()
main_font.setPointSize(17)

class Widget(QtWidgets.QWidget):
    def __init__(self, directory, job_id, parent):
        super(Widget, self).__init__()
        self.directory = str(directory)
        self.job_id = job_id
        self.constrct_ui()

    def constrct_ui(self):
        print ("Hi")
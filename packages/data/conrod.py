from PySide2 import QtCore, QtGui, QtWidgets
from packages.backend import connection

class Widget(QtWidgets.QWidget):
    def __init__(self, directory, job_id, parent=None):
        super(Widget, self).__init__()
        self.setObjectName("conrod")
        self.directory = str(directory)
        self.job_id = job_id
        self.construct_ui()

    def construct_ui(self):
        return
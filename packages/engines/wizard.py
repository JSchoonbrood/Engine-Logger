import sqlite3
import os
from PySide2 import QtCore, QtGui, QtWidgets

class AddWindow(QtWidgets.QMainWindow):
    db_signal = QtCore.Signal()
    def __init__(self, directory, parent):
        super(AddWindow, self).__init__()
        self.directory = str(directory)
        self.database = os.path.join(self.directory, 'Engines.db')
        self.constrct_ui()

    def constrct_ui(self):
        self.setWindowTitle("Engine Logger - Wizard")
        resolution = QtWidgets.QDesktopWidget().availableGeometry()
        self.setGeometry(0, 0, resolution.width()/3, resolution.height()/4)

        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, -1, -1))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")

        self.title = QtWidgets.QLabel("Title *")
        self.gridLayout.addWidget(self.title, 0, 0, 1, 1)

        self.vehicle = QtWidgets.QLabel("Car")
        self.gridLayout.addWidget(self.vehicle, 1, 0, 1, 1)
        
        self.engine = QtWidgets.QLabel("Engine")
        self.gridLayout.addWidget(self.engine, 2, 0, 1, 1)

        self.build_date = QtWidgets.QLabel("Build Date")
        self.gridLayout.addWidget(self.build_date, 3, 0, 1, 1)

        self.built_by = QtWidgets.QLabel("Built By")
        self.gridLayout.addWidget(self.built_by, 4, 0, 1, 1)

        self.customer = QtWidgets.QLabel("Customer")
        self.gridLayout.addWidget(self.customer, 5, 0, 1, 1)

        self.title_entry = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.title_entry, 0, 1, 1, 1)

        self.vehicle_entry = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.vehicle_entry, 1, 1, 1, 1)

        self.engine_entry = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.engine_entry, 2, 1, 1, 1)

        self.build_date_entry = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.build_date_entry, 3, 1, 1, 1)

        self.built_by_entry = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.built_by_entry, 4, 1, 1, 1)

        self.customer_entry = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.customer_entry, 5, 1, 1, 1)

        self.add_button = QtWidgets.QPushButton()
        self.add_button.clicked.connect(self.populate_database)
        self.add_button.setText("Add Job")
        self.gridLayout.addWidget(self.add_button, 6, 0, 1, 2)

        self.setCentralWidget(self.gridLayoutWidget)

    def populate_database(self):
        connection = sqlite3.connect(self.database)

        title = self.title_entry.text()
        vehicle = self.vehicle_entry.text()
        engine = self.engine_entry.text()
        build_date = self.build_date_entry.text()
        built_by = self.built_by_entry.text()
        customer = self.customer_entry.text()

        if not title == "":
            cursor = connection.cursor()
            cursor.execute(
                '''INSERT INTO Engine(title, car, engine, build_date, built_by, customer)VALUES(?, ?, ?, ?, ?, ?)''',(title, vehicle, engine, build_date, built_by, customer)
            )
            connection.commit()
            connection.close()

            self.title_entry.clear()
            self.engine_entry.clear()
            self.vehicle_entry.clear()
            self.customer_entry.clear()
            self.build_date_entry.clear()
            self.built_by_entry.clear()

            self.db_signal.emit()
            

import sqlite3
import os
from PySide2 import QtCore, QtGui, QtWidgets
from packages.engines import wizard

button_font = QtGui.QFont()
button_font.setPointSize(17)

table_header_font = QtGui.QFont()
table_header_font.setPointSize(15)

table_font = QtGui.QFont()
table_font.setPointSize(13)

class Widget(QtWidgets.QWidget):
    checklist_signal = QtCore.Signal(int)
    def __init__(self, directory, parent):
        super(Widget, self).__init__()
        self.directory = str(directory)
        self.database = os.path.join(self.directory, 'Engines.db')
        self.constrct_ui()
        self.read_database()

    def constrct_ui(self):
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")

        # Header Layout
        self.header_widget = QtWidgets.QWidget()
        
        self.header_widget.setGeometry(QtCore.QRect(0, 0, -1, -1))
        self.header_widget.setObjectName("header_widget")

        self.header_layout = QtWidgets.QGridLayout(self.header_widget)
        self.header_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.header_layout.setObjectName("header_layout")

        self.engines_button = QtWidgets.QPushButton()
        self.engines_button.setFont(button_font)
        self.engines_button.setObjectName("engines_button")
        self.engines_button.setText("Engines")
        self.header_layout.addWidget(self.engines_button, 0, 0, 1, 1)

        self.procedures_button = QtWidgets.QPushButton()
        self.procedures_button.setFont(button_font)
        self.procedures_button.setObjectName("procedures_button")
        self.procedures_button.setText("Procedures")
        self.header_layout.addWidget(self.procedures_button, 0, 1, 1, 1)

        self.manuals_button = QtWidgets.QPushButton()
        self.manuals_button.setFont(button_font)
        self.manuals_button.setObjectName("manuals_button")
        self.manuals_button.setText("Manuals")
        self.header_layout.addWidget(self.manuals_button, 0, 2, 1, 1)

        self.gallery_button = QtWidgets.QPushButton()
        self.gallery_button.setFont(button_font)
        self.gallery_button.setObjectName("gallery_button")
        self.gallery_button.setText("Gallery")
        self.header_layout.addWidget(self.gallery_button, 0, 3, 1, 1)

        self.settings_button = QtWidgets.QPushButton()
        self.settings_button.setFont(button_font)
        self.settings_button.setObjectName("settings_button")
        self.settings_button.setText("Settings")
        self.header_layout.addWidget(self.settings_button, 0, 4, 1, 1)

        self.header_widget.setLayout(self.header_layout)
        self.gridLayout.addWidget(self.header_widget, 0, 0, 1, 5)

        # Main Body

        self.engines = QtWidgets.QTableWidget()
        self.engines.setFont(table_font)
        self.engines.setFocusPolicy(QtCore.Qt.NoFocus)
        self.engines.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.engines.verticalHeader().setVisible(False)
        self.engines.setColumnCount(5)
        self.engines.setHorizontalHeaderLabels(['ID', 'Title', 'Engine Code', 'Car', 'Customer'])

        header = self.engines.horizontalHeader()
        header.setFont(table_header_font)
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.engines.clicked.connect(self.send_data)

        self.gridLayout.addWidget(self.engines, 1, 0, 1, 5)

        # Footer

        self.add_button = QtWidgets.QPushButton()
        self.add_button.setObjectName("add_button")
        self.add_button.setText("Add Job")
        self.add_button.clicked.connect(self.call_window)

        self.gridLayout.addWidget(self.add_button, 2, 0, 1, 5)

        self.setLayout(self.gridLayout) # Add This Line Manually
        return

    def table_item(self, item):
        new_item = QtWidgets.QTableWidgetItem(item)
        new_item.setFlags(new_item.flags() ^ QtCore.Qt.ItemIsEditable)
        return new_item

    def read_database(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        cursor.execute('''SELECT * FROM Engine''')
        index = 0
        for row in cursor.fetchall():
            self.engines.setRowCount(index+1)
            for i in range(5):
                self.engines.setItem(index, i, self.table_item(str(row[i])))
            index += 1
        
        cursor.close()

        self.engines.setColumnHidden(0, True)
        return

    def call_window(self):
        self.add_window = wizard.AddWindow(self.directory, self)
        self.add_window.db_signal.connect(self.update_database)
        self.add_window.show()
        return

    def send_data(self, index):
        job_id = index.sibling(index.row(), 0).data()
        self.checklist_signal.emit(int(job_id))
        return

    @QtCore.Slot()
    def update_database(self):
        self.read_database()
        return

    
        
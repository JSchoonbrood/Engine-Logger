import os
from PySide2 import QtCore, QtGui, QtWidgets
from packages.backend import connection

class Widget(QtWidgets.QWidget):
    IdRole = QtCore.Qt.UserRole + 1000
    title_signal = QtCore.Signal(str)
    def __init__(self, directory, job_id, parent):
        super(Widget, self).__init__()
        self.directory = str(directory)
        self.job_id = job_id
        self.constrct_ui()
        self.populate_menu()

    def constrct_ui(self):
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        self.grid_layout.setSpacing(5)
        self.grid_layout.setObjectName("grid_layout")

        self.menu = QtWidgets.QComboBox()
        self.menu_model = QtGui.QStandardItemModel()
        self.menu.currentIndexChanged.connect(self.id_updated)

        self.block_label = QtWidgets.QLabel("Engine Block")

        self.head_label = QtWidgets.QLabel("Cylinderhead")

        self.ancillaries_label = QtWidgets.QLabel("Ancillaries")

        self.electrical_label = QtWidgets.QLabel("Electrical")

        self.notes_label = QtWidgets.QLabel("Notes")

        self.grid_layout.addWidget(self.menu, 0, 0, 1, 5)

        self.setLayout(self.grid_layout)

    def populate_menu(self):
        database = connection.Query(self.directory, self)
        cursor = database.query('''SELECT * From Engine''')

        index_counter = 0
        for row in cursor.fetchall():
            item = QtGui.QStandardItem(row[1])
            item.setData(row[0], self.IdRole)
            if row[0] == self.job_id:
                current_index = index_counter
            index_counter += 1
            self.menu_model.appendRow(item)
        self.menu.setModel(self.menu_model)
        database.close()

        self.menu.setCurrentIndex(current_index)

    def reset_menu(self):
        self.menu.clear()

    def current_id(self, index):
        id = self.menu.itemData(index, self.IdRole)

    def id_updated(self, index):
        id = self.menu.itemData(index, self.IdRole)
        self.job_id = id
        database = connection.Query(self.directory, self)
        cursor = database.query('''SELECT * From Engine WHERE id = ?''', self.job_id)

        data = cursor.fetchone()
        self.title_signal.emit(str(data[1]))

        # Update Ticked Checkboxes, Times, Prices
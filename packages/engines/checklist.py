import os
from PySide2 import QtCore, QtGui, QtWidgets
from packages.backend import connection

title_font = QtGui.QFont()
title_font.setPointSize(18)

main_font = QtGui.QFont()
main_font.setPointSize(17)

class Widget(QtWidgets.QWidget):
    IdRole = QtCore.Qt.UserRole + 1000
    title_signal = QtCore.Signal(str)
    widget_signal = QtCore.Signal(object)
    def __init__(self, directory, job_id, parent):
        super(Widget, self).__init__()
        self.directory = str(directory)
        self.job_id = job_id
        self.constrct_ui()
        self.populate_menu()

    def constrct_ui(self):
        self.vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        self.grid_layout.setSpacing(5)
        self.grid_layout.setObjectName("grid_layout")

        self.menu = QtWidgets.QComboBox()
        self.menu.setFont(title_font)
        self.menu_model = QtGui.QStandardItemModel()
        self.menu.currentIndexChanged.connect(self.id_updated)

        # Engine Block

        self.block_label = QtWidgets.QLabel("Engine Block")
        self.block_label.setFont(title_font)
        self.block_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.block_label, 1, 0, 1, 1)

        self.block_widget = QtWidgets.QWidget()
        self.block_layout = QtWidgets.QGridLayout()
        self.block_layout.setColumnMinimumWidth(0, 1)

        self.procedures = QtWidgets.QLabel("Procedures")
        self.procedures.setAlignment(QtCore.Qt.AlignLeft)
        self.procedures.setFont(main_font)
        self.block_layout.addWidget(self.procedures, 0, 0, 1, 2)

        self.time = QtWidgets.QLabel("Time")
        self.time.setFont(main_font)
        self.block_layout.addWidget(self.time, 0, 3, 1, 1)

        self.cost = QtWidgets.QLabel("Cost")
        self.cost.setFont(main_font)
        self.cost.setAlignment(QtCore.Qt.AlignCenter)
        self.block_layout.addWidget(self.cost, 0, 4, 1, 1)

        self.block_checkbox = QtWidgets.QCheckBox()
        self.block_layout.addWidget(self.block_checkbox, 1, 0, 1, 1)
        self.block_clearances = QtWidgets.QPushButton("Block")
        self.block_clearances.setObjectName("Block")
        self.block_clearances.clicked.connect(lambda: self.widget_change(self.block_clearances))
        self.block_clearances.setMaximumSize(self.block_clearances.sizeHint())
        self.block_clearances.setFont(main_font)
        self.block_layout.addWidget(self.block_clearances, 1, 1, 1, 1)

        self.piston_checkbox = QtWidgets.QCheckBox()
        self.block_layout.addWidget(self.piston_checkbox, 2, 0, 1, 1)
        self.piston_label = QtWidgets.QLabel("Pistons")
        self.piston_label.setFont(main_font)
        self.block_layout.addWidget(self.piston_label, 2, 1, 1, 1)

        self.conrods_checkbox = QtWidgets.QCheckBox()
        self.block_layout.addWidget(self.conrods_checkbox, 3, 0, 1, 1)
        self.conrods_label = QtWidgets.QLabel("ConRods")
        self.conrods_label.setFont(main_font)
        self.block_layout.addWidget(self.conrods_label, 3, 1, 1, 1)

        self.balancing_checkbox = QtWidgets.QCheckBox()
        self.block_layout.addWidget(self.balancing_checkbox, 4, 0, 1, 1)
        self.balancing_label = QtWidgets.QLabel("Balancing")
        self.balancing_label.setFont(main_font)
        self.block_layout.addWidget(self.balancing_label, 4, 1, 1, 1)

        self.crank_checkbox = QtWidgets.QCheckBox()
        self.block_layout.addWidget(self.crank_checkbox, 5, 0, 1, 1)
        self.crank_label = QtWidgets.QLabel("Crank & Bearings")
        self.crank_label.setFont(main_font)
        self.block_layout.addWidget(self.crank_label, 5, 1, 1, 1)

        self.oilpump_checkbox = QtWidgets.QCheckBox()
        self.block_layout.addWidget(self.oilpump_checkbox, 6, 0, 1, 1)
        self.oilpump_label = QtWidgets.QLabel("Oil Pump")
        self.oilpump_label.setFont(main_font)
        self.block_layout.addWidget(self.oilpump_label, 6, 1, 1, 1)

        self.parts_used = QtWidgets.QLabel("Parts Cost")
        self.parts_used.setFont(main_font)
        self.block_layout.addWidget(self.parts_used, 7, 1, 1, 1)

        self.external_costs = QtWidgets.QLabel("List Of External Costs")
        self.external_costs.setFont(main_font)
        self.block_layout.addWidget(self.external_costs, 8, 1, 1, 1)

        self.block_layout.addItem(self.vertical_spacer, 9, 0, 1, 4)
        self.block_layout.addItem(self.vertical_spacer, 0, 2, 8, 1)

        self.block_widget.setLayout(self.block_layout)
        self.grid_layout.addWidget(self.block_widget, 3, 0, 4, 1)

        # Cylinder Head

        self.head_label = QtWidgets.QLabel("Cylinderhead")
        self.head_label.setFont(title_font)
        self.head_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.head_label, 1, 1, 1, 1)

        self.head_widget = QtWidgets.QWidget()
        self.head_layout = QtWidgets.QGridLayout()
        self.head_layout.setColumnMinimumWidth(0, 1)

        self.procedures = QtWidgets.QLabel("Procedures")
        self.procedures.setAlignment(QtCore.Qt.AlignLeft)
        self.procedures.setFont(main_font)
        self.head_layout.addWidget(self.procedures, 0, 0, 1, 2)

        self.time = QtWidgets.QLabel("Time")
        self.time.setFont(main_font)
        self.head_layout.addWidget(self.time, 0, 3, 1, 1)

        self.cost = QtWidgets.QLabel("Cost")
        self.cost.setFont(main_font)
        self.cost.setAlignment(QtCore.Qt.AlignCenter)
        self.head_layout.addWidget(self.cost, 0, 4, 1, 1)

        self.cylhead_checkbox = QtWidgets.QCheckBox()
        self.head_layout.addWidget(self.cylhead_checkbox, 1, 0, 1, 1)
        self.cylhead_label = QtWidgets.QLabel("Cylinder Head")
        self.cylhead_label.setFont(main_font)
        self.head_layout.addWidget(self.cylhead_label, 1, 1, 1, 1)

        self.intcam_checkbox = QtWidgets.QCheckBox()
        self.head_layout.addWidget(self.intcam_checkbox, 2, 0, 1, 1)
        self.intcam_label = QtWidgets.QLabel("Intake Camshaft 1")
        self.intcam_label.setFont(main_font)
        self.head_layout.addWidget(self.intcam_label, 2, 1, 1, 1)

        self.exhcam_checkbox = QtWidgets.QCheckBox()
        self.head_layout.addWidget(self.exhcam_checkbox, 3, 0, 1, 1)
        self.exhcam_label = QtWidgets.QLabel("Exhaust Camshaft 1")
        self.exhcam_label.setFont(main_font)
        self.head_layout.addWidget(self.exhcam_label, 3, 1, 1, 1)

        self.head_layout.addItem(self.vertical_spacer, 9, 0, 1, 4)
        self.head_layout.addItem(self.vertical_spacer, 0, 2, 8, 1)
        self.head_widget.setLayout(self.head_layout)
        self.grid_layout.addWidget(self.head_widget, 3, 1, 4, 1)

        # Extras

        self.extras_label = QtWidgets.QLabel("Extras")
        self.extras_label.setFont(title_font)
        self.extras_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.extras_label, 1, 2, 1, 1)

        self.grid_layout.addWidget(self.menu, 0, 0, 1, 3)
        self.grid_layout.addItem(self.vertical_spacer, 3, 0, 1, 3)

        self.setLayout(self.grid_layout)

    def populate_menu(self):
        database = connection.Query(self.directory, self)
        cursor = database.query('''SELECT * From Jobs''')

        remove_char = "()',"

        index_counter = 0
        for row in cursor.fetchall():
            title = ''.join((str(row[1:5])))
            for char in remove_char:
                title = title.replace(char, "")
            item = QtGui.QStandardItem(title)
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
        cursor = database.query('''SELECT * From Jobs WHERE job_id = ?''', (self.job_id,))

        data = cursor.fetchone()
        self.title_signal.emit(str(data[1]))

        database.close()

        # Update Ticked Checkboxes, Times, Prices

    def widget_change(self, object):
        widget_name = object.objectName()
        self.widget_signal.emit((widget_name, self.job_id))
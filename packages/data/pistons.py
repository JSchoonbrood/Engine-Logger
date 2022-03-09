from PySide2 import QtCore, QtGui, QtWidgets
from packages.backend import connection

class Widget(QtWidgets.QWidget):
    def __init__(self, directory, job_id, parent=None):
        super(Widget, self).__init__()
        self.setObjectName("pistons")
        self.directory = str(directory)
        self.job_id = job_id
        self.constrct_ui()

    def constrct_ui(self):
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        self.grid_layout.setSpacing(5)

        # Row 1
        self.make_label = QtWidgets.QLabel("Piston Make")
        self.make_input = QtWidgets.QLineEdit()

        # Row 2
        self.diameter_label = QtWidgets.QLabel("Piston Diameter")
        self.piston_diameter_input = QtWidgets.QLineEdit()

        self.clearance_label = QtWidgets.QLabel("Piston Clearance")
        self.clearance_input = QtWidgets.QLineEdit()

        self.weight_label = QtWidgets.QLabel("Piston Weight WOut/ Pin")
        self.weight_input = QtWidgets.QLineEdit()
        
        # Row 3
        self.wristpin_weight_label = QtWidgets.QLabel("Wristpin Weight")
        self.wristpin_weight_input = QtWidgets.QLineEdit()

        self.wristpin_od_label = QtWidgets.QLabel("Wristpin Outer Diameter")
        self.wristpin_od_input = QtWidgets.QLineEdit()

        self.ring_table = QtWidgets.QTableWidget()
        vertical_labels = ['Ring Type', 'Ring Thickness', 'Ring Gap']
        hor_labels = ['Top Ring', 'Second Ring', 'Oil Ring']

        self.ring_table.setRowCount(3)
        self.ring_table.setVerticalHeaderLabels(vertical_labels)
        self.ring_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ring_table.setColumnCount(3)
        self.ring_table.setHorizontalHeaderLabels(hor_labels) 
        self.ring_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        #self.grid_layout.addWidget(self.ring_table)


        # Add Widgets To Layout
        self.grid_layout.addWidget(self.make_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.make_input, 0, 1, 1, 2)

        self.grid_layout.addWidget(self.diameter_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.piston_diameter_input, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.clearance_label, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.clearance_input, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.weight_label, 1, 2, 1, 1)
        self.grid_layout.addWidget(self.weight_input, 2, 2, 1, 1)

        self.grid_layout.addWidget(self.wristpin_weight_label, 4, 0, 1, 1)
        self.grid_layout.addWidget(self.wristpin_weight_input, 5, 0, 1, 1)
        self.grid_layout.addWidget(self.wristpin_od_label, 4, 1, 1, 1)
        self.grid_layout.addWidget(self.wristpin_od_input, 5, 1, 1, 1)

        self.grid_layout.addWidget(self.ring_table, 6, 0, 1, 3)

        # Set Layouts
        self.setLayout(self.grid_layout)
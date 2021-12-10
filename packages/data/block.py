from PySide2 import QtCore, QtGui, QtWidgets
from packages.backend import connection

title_font = QtGui.QFont()
title_font.setPointSize(18)

main_font = QtGui.QFont()
main_font.setPointSize(17)

class Widget(QtWidgets.QWidget):
    def __init__(self, directory, job_id, parent=None):
        super(Widget, self).__init__()
        self.directory = str(directory)
        self.job_id = job_id
        self.constrct_ui()

    def constrct_ui(self):
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        self.grid_layout.setSpacing(5)
        self.grid_layout.setObjectName("grid_layout")

        # Row 1

        self.make_label = QtWidgets.QLabel("Engine Make")
        self.make_label.setFont(main_font)
        self.make_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.make_label, 0, 0, 1, 1)

        self.make_input = QtWidgets.QLineEdit()
        self.grid_layout.addWidget(self.make_input, 0, 1, 1, 1)

        self.type_label = QtWidgets.QLabel("Engine Type")
        self.type_label.setFont(main_font)
        self.type_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.type_label, 0, 2, 1, 1)

        self.type_dropdown = QtWidgets.QComboBox()
        self.type_dropdown.addItems(["Inline", "V-Type", "W-Type", "Wankel (Rotary)", "2Stroke", "Radial"])
        self.grid_layout.addWidget(self.type_dropdown, 0, 3, 1, 1)

        self.engine_code_label = QtWidgets.QLabel("Engine Code")
        self.engine_code_label.setFont(main_font)
        self.engine_code_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.engine_code_label, 0, 4, 1, 1)

        self.engine_code_input = QtWidgets.QLineEdit()
        self.grid_layout.addWidget(self.engine_code_input, 0, 5, 1, 1)

        self.notes = QtWidgets.QTextEdit()
        self.grid_layout.addWidget(self.notes, 0, 6, 5, 1)
        
        # Row 4

        self.table_data = QtWidgets.QTableWidget()

        # Row 2

        self.cylinders_label = QtWidgets.QLabel("No. Of Cylinders")
        self.cylinders_label.setFont(main_font)
        self.cylinders_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.cylinders_label, 1, 0, 1, 1)

        self.cylinders_input = QtWidgets.QComboBox()
        self.cylinders_input.currentIndexChanged.connect(self.setup_table)

        for i in range(16):
            self.cylinders_input.addItem(str(i+1))

        self.cylinders_input.setCurrentIndex(3)

        self.grid_layout.addWidget(self.cylinders_input, 1, 1, 1, 1)

        self.compratio_label = QtWidgets.QLabel("Compression Ratio")
        self.compratio_label.setFont(main_font)
        self.compratio_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.compratio_label, 1, 2, 1, 1)

        self.compratio = QtWidgets.QLineEdit()
        self.grid_layout.addWidget(self.compratio, 1, 3, 1, 1)

        self.cc_label = QtWidgets.QLabel("CC")
        self.cc_label.setFont(main_font)
        self.cc_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.cc_label, 1, 4, 1, 1)

        self.cc_input = QtWidgets.QLineEdit()
        self.grid_layout.addWidget(self.cc_input, 1, 5, 1, 1)

        # Row 3

        self.stroke_label = QtWidgets.QLabel("Stroke")
        self.stroke_label.setFont(main_font)
        self.stroke_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.stroke_label, 2, 2, 1, 1)

        self.stroke_input = QtWidgets.QLineEdit()
        self.grid_layout.addWidget(self.stroke_input, 2, 3, 1, 1)

        self.bore_label = QtWidgets.QLabel("Bore Size")
        self.bore_label.setFont(main_font)
        self.bore_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.bore_label, 3, 0, 1, 1)

        self.bore_input = QtWidgets.QLineEdit()
        self.grid_layout.addWidget(self.bore_input, 3, 1, 1, 1)

        self.liner_label = QtWidgets.QLabel("Liner Protrusion")
        self.liner_label.setFont(main_font)
        self.liner_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.liner_label, 3, 2, 1, 1)

        self.liner_input = QtWidgets.QLineEdit()
        self.grid_layout.addWidget(self.liner_input, 3, 3, 1, 1)

        self.tunnel_label = QtWidgets.QLabel("Main Tunnel Size")
        self.tunnel_label.setFont(main_font)
        self.tunnel_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.tunnel_label, 3, 4, 1, 1)

        self.tunnel_input = QtWidgets.QLineEdit()
        self.grid_layout.addWidget(self.tunnel_input, 3, 5, 1, 1)

        # self.table_data needs to be initialised before self.cylinders_input
        self.setup_table()
        self.grid_layout.addWidget(self.table_data, 4, 0, 1, 6)
        self.cylinders_input.currentIndexChanged.connect(self.setup_table)

        self.setLayout(self.grid_layout)

    def setup_table(self):
        columns = self.cylinders_input.currentText()
        self.table_data.setColumnCount(int(columns))

        hor_labels = []
        for i in range(int(columns)):
            name = "Cyl " + str(i+1)
            hor_labels.append(name)
        self.table_data.setHorizontalHeaderLabels(hor_labels)

        ver_labels = ['Top Bore Size', 'Middle Bore Size', 'Lower Bore Size', 'Total Difference', 'Oval?']
        self.table_data.setRowCount(5)
        self.table_data.setVerticalHeaderLabels(ver_labels)

        hor_header = self.table_data.horizontalHeader()
        #header.setFont(table_header_font)
        hor_header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        ver_header = self.table_data.verticalHeader()
        ver_header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)




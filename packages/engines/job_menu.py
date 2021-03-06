import os
from PySide2 import QtCore, QtGui, QtWidgets
from packages.backend import connection
from packages.data import block
from packages.data import pistons

class Widget(QtWidgets.QWidget):
    IdRole = QtCore.Qt.UserRole + 1000
    job_id_signal = QtCore.Signal(str)
    def __init__(self, directory, job_id, parent):
        super(Widget, self).__init__()
        self.directory = str(directory)
        self.job_id = job_id
        self.setObjectName("job-menu")
        self.constrct_ui()
        self.populate_menu()
        
    def constrct_ui(self):
        # Miscellaneous

        #self.spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # Layouts

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setObjectName("main-layout")
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        self.grid_layout.setSpacing(5)

        self.block_widget = QtWidgets.QWidget()
        self.block_widget.setObjectName("background")
        self.block_layout = QtWidgets.QVBoxLayout()
        self.block_layout.setContentsMargins(0, 0, 0, 0)
        self.block_layout.setSpacing(1)

        # Job Switcher

        self.menu = QtWidgets.QComboBox()
        self.menu.setObjectName("jobswitcher")
        self.menu_model = QtGui.QStandardItemModel()
        self.menu.currentIndexChanged.connect(self.id_updated)
        self.menu.setFocusPolicy(QtCore.Qt.NoFocus)

        # Menu Buttons
        
        self.block_clearances = QtWidgets.QPushButton("Block")
        self.block_clearances.setObjectName("Block")
        self.block_clearances.clicked.connect(lambda: self.widget_change(self.block_clearances))
        self.block_clearances.setFocus()

        self.piston_label = QtWidgets.QPushButton("Pistons")
        self.piston_label.setObjectName("Piston")
        self.piston_label.clicked.connect(lambda: self.widget_change(self.piston_label))
        
        self.conrods_label = QtWidgets.QPushButton("ConRods")
        
        self.balancing_label = QtWidgets.QPushButton("Balancing")
        
        self.crank_label = QtWidgets.QPushButton("Crank / Bearings")
        
        self.oilpump_label = QtWidgets.QPushButton("Oil Pump")
        
        self.cylhead_label = QtWidgets.QPushButton("Cylinder Head")
        
        self.intcam_label = QtWidgets.QPushButton("Intake Cam")
        
        self.exhcam_label = QtWidgets.QPushButton("Exhaust Cam")

        # Main Windows

        self.block = block.Widget(self.directory, self.job_id, self)
        self.pistons = pistons.Widget(self.directory, self.job_id, self)

        # Main Window Stack

        self.stack = QtWidgets.QStackedWidget()

        self.stack.addWidget(self.block)
        self.stack.addWidget(self.pistons)

        self.stack.setCurrentWidget(self.block)

        # Scale Buttons
        
        screen = QtWidgets.QApplication.primaryScreen() # .instance() alternative
        width = screen.availableGeometry().width()
        height = screen.availableGeometry().height()
        
        button_width = width/7

        self.block_clearances.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.piston_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.conrods_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.balancing_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.crank_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.oilpump_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.cylhead_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.intcam_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.exhcam_label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

        self.block_clearances.setMaximumWidth(button_width)
        self.piston_label.setMaximumWidth(button_width)
        self.conrods_label.setMaximumWidth(button_width)
        self.balancing_label.setMaximumWidth(button_width)
        self.crank_label.setMaximumWidth(button_width)
        self.oilpump_label.setMaximumWidth(button_width)
        self.cylhead_label.setMaximumWidth(button_width)
        self.intcam_label.setMaximumWidth(button_width)
        self.exhcam_label.setMaximumWidth(button_width)

        # Add Widgets To Layout

        self.block_layout.addWidget(self.block_clearances)
        self.block_layout.addWidget(self.piston_label)
        self.block_layout.addWidget(self.conrods_label)
        self.block_layout.addWidget(self.balancing_label)
        self.block_layout.addWidget(self.crank_label)
        self.block_layout.addWidget(self.oilpump_label)
        self.block_layout.addWidget(self.cylhead_label)
        self.block_layout.addWidget(self.intcam_label)
        self.block_layout.addWidget(self.exhcam_label)
        
        # Set Layouts

        self.block_widget.setLayout(self.block_layout)

        self.grid_layout.addWidget(self.menu, 0, 0, 1, 3)
        self.grid_layout.addWidget(self.stack, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.block_widget, 1, 2, 1, 1)

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
        self.job_id_signal.emit(str(data[1]))

        database.close()

        # Update Ticked Checkboxes, Times, Prices

    def widget_change(self, object):
        page = object.objectName()
        
        if page == "Block":
            self.stack.setCurrentWidget(self.block)
        elif page == "Piston":
            self.stack.setCurrentWidget(self.pistons)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QHBoxLayout
from PyQt5.QtGui import *
from Graph import make_graph
from datetime import datetime, timedelta
from Data import Data


class TimeSlider(QWidget):
    # implementacja suwaka do czasu

    def __init__(self, data_range, parent, type):
        super().__init__()

        self.initUI(data_range)
        self.__parent = parent
        self.__type = type

    def initUI(self, data_range):
        hbox = QHBoxLayout()

        sld = QSlider(Qt.Horizontal, self)
        sld.setRange(0, data_range)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setPageStep(5)

        sld.valueChanged.connect(self.__update_label)

        self.label = QLabel('22-01-2020', self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)
        self.setStyleSheet(
            "selection-color : rgb(196,245,95);"
        )

        hbox.addWidget(sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 350, 250)

    def __update_label(self, value):
        date_format = '%d-%m-%Y'
        date = str(datetime.strptime('22-01-2020', date_format) + timedelta(value))
        self.label.setText(date[:10])
        Data.START_DAY = int(value)
        Data.DAY = date[:10]
        make_graph(self.__type, self.__parent)

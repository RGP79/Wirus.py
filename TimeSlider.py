from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import *
from Graph import make_graph
from datetime import datetime, timedelta

from Exceptions import ErrorWindow
from Wirus_git.Wirus_clone.Graph import ReadLen


class SliderWindow(QWidget):
    def __init__(self, data_range, parent, type):
        super().__init__()
        self.__create_window(data_range, parent, type)

    def __create_window(self, data_range, parent, type):
        vbox = QVBoxLayout()
        lower_slider = LowerTimeSlider(data_range, parent, type)
        upper_slider = UpperTimeSlider(data_range, parent, type)
        vbox.addWidget(lower_slider)
        vbox.addSpacing(5)
        vbox.setGeometry(QRect(1000, 60, 1000, 60))
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(upper_slider)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 1000, 60)



class TimeSlider(QWidget):
    # implementacja suwaka do czasu

    def __init__(self, data_range, name):
        super().__init__()
        self.__name = name
        self.sld = QSlider(Qt.Horizontal, self)
        self.initUI(data_range)

    def initUI(self, data_range):
        hbox = QHBoxLayout()

        self.sld.setRange(0, data_range - 2)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setPageStep(5)
        self.label = QLabel(self.__name, self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(20)
        self.setStyleSheet(
            "selection-color : rgb(196,245,95);"
        )

        hbox.addWidget(self.sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)


class LowerTimeSlider(TimeSlider):

    def __init__(self, data_range, parent, type):
        super().__init__(data_range, parent.Data.FIRST_DATE)
        self.sld.valueChanged.connect(self.__update_label)
        self.__parent = parent
        self.__type = type
        self.sld.setTickPosition(2)
        self.sld.setSliderPosition(0)

    def __update_label(self, value):
        try:
            date_format = '%Y-%m-%d'
            print(self.__parent.Data.FIRST_DATE)
            date = str(datetime.strptime(self.__parent.Data.FIRST_DATE, date_format) + timedelta(value))
            self.label.setText(date[:10])
            self.__parent.Data.START_DAY = int(value)
            self.__parent.Data.FIRST_PDF_DATE = date[:10]
            make_graph(self.__type, self.__parent)
        except:
            ErrorWindow("Brak wczytanego pliku!")


class UpperTimeSlider(TimeSlider):

    def __init__(self, data_range, parent, type):
        super().__init__(data_range, parent.Data.LAST_DATE)
        self.sld.valueChanged.connect(self.__update_label)
        self.__parent = parent
        self.end = data_range
        self.__type = type
        self.sld.setTickPosition(1)
        self.sld.setInvertedAppearance(True)

    def __update_label(self, value):
        try:
            date_format = '%Y-%m-%d'
            date = str(datetime.strptime(self.__parent.Data.LAST_DATE, date_format) - timedelta(value))
            self.label.setText(date[:10])
            self.__parent.Data.END_DAY = self.end - int(value)
            self.__parent.Data.END_PDF_DATE = date[:10]
            make_graph(self.__type, self.__parent)
        except:
            ErrorWindow("Brak wczytanego pliku!")


class update_sliders:
    def __init__(self, parent,type):
        self.__type = type
        self.__parent = parent
        self.__cos()

    def __cos(self):
        try:
            print(f"to jest end day {self.__parent.Data.END_DAY}")
            data_range = ReadLen(self.__parent.Data.FILENAME).get_len()
            slider = SliderWindow(data_range, self.__parent, self.__type)
            self.__parent.main_layout.removeWidget(self.__parent.get_slider())
            self.__parent.main_layout.addWidget(slider, 4, 0, 1, 3)
            self.__parent.setLayout(self.__parent.main_layout)
        except:
            ErrorWindow("Nie wybrano Pliku lub Państw!")
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import *
from Graph import UpdateGraph
from datetime import datetime, timedelta
from File_service import ReadLen
from Look_Config import Config
from Exceptions import Warning


class SliderWindow(QWidget):
    def __init__(self, data_range, parent):
        super().__init__()
        self.__create_window(data_range, parent)

    def __create_window(self, data_range, parent):
        vbox = QVBoxLayout()
        self.lower_slider = LowerTimeSlider(data_range, parent)
        self.upper_slider = UpperTimeSlider(data_range, parent)
        vbox.addWidget(self.lower_slider)
        vbox.addSpacing(5)
        vbox.setGeometry(QRect(1000, 60, 1000, 60))
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(self.upper_slider)
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
        self.setStyleSheet(Config.SLIDER)

        hbox.addWidget(self.sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)


class LowerTimeSlider(TimeSlider):

    def __init__(self, data_range, parent):
        super().__init__(data_range, parent.Data.get_first_date())
        self.sld.valueChanged.connect(self.__update_label)
        self.__parent = parent

        self.sld.setTickPosition(2)
        self.sld.setSliderPosition(0)

    def __update_label(self, value):
        try:
            date_format = '%Y-%m-%d'
            date = str(datetime.strptime(self.__parent.Data.get_first_date(), date_format) + timedelta(value))
            self.label.setText(date[:10])
            self.__parent.Data.set_start_day(int(value))
            self.__parent.Data.set_start_pdf_date(date[:10])
            UpdateGraph(self.__parent)
            if self.__parent.Data.get_start_day() - 3 > self.__parent.Data.get_end_day():
                self.sld.setValue(self.__parent.Data.get_end_day() - 3)
        except:
            Warning("Brak wczytanego pliku!")


class UpperTimeSlider(TimeSlider):

    def __init__(self, data_range, parent):
        super().__init__(data_range, parent.Data.get_last_date())
        self.sld.valueChanged.connect(self.__update_label)
        self.__parent = parent
        self.end = data_range

        self.sld.setTickPosition(1)
        self.sld.setInvertedAppearance(True)

    def __update_label(self, value):
        try:
            date_format = '%Y-%m-%d'
            date = str(datetime.strptime(self.__parent.Data.get_last_date(), date_format) - timedelta(value))
            self.label.setText(date[:10])
            self.__parent.Data.set_end_day(self.end - int(value))
            self.__parent.Data.set_end_pdf_date(date[:10])
            UpdateGraph(self.__parent)
            if self.__parent.Data.get_end_day() < self.__parent.Data.get_start_day():
                self.sld.setValue(self.end - self.__parent.Data.get_start_day() - 3)
        except:
            Warning("Brak wczytanego pliku!")


class UpdateSliders:
    def __init__(self, parent):

        self.__parent = parent
        self.__update()

    def __update(self):
        try:
            data_range = ReadLen(self.__parent.Data.get_filename()).get_len()
            slider = SliderWindow(data_range, self.__parent)
            self.__parent.Data.set_end_day(slider.upper_slider.end)
            self.__parent.Data.set_start_day(0)
            self.__parent.main_layout.removeWidget(self.__parent.get_slider())
            self.__parent.main_layout.addWidget(slider, 4, 0, 1, 4)
            self.__parent.setLayout(self.__parent.main_layout)
        except:
            Warning("Nie wybrano pliku lub państw!")

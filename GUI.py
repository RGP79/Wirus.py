import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, \
    QFileDialog, QMainWindow, QTabWidget
from PyQt5.QtGui import *


from Country_box import CountryBox
from File_service import ReadCountries, ReadLen, FirstDay, EndDay
from Pdf_maker import PDFButton
from SearchPanel import SearchPanel
from TimeSlider import SliderWindow
from ResetButton import ResetButton
from Data import Data
from Look_Config import Config
from CheckMode import PlotBox
from Exceptions import Warning
from Graph import Semilogy


class InputDataButton(QPushButton):
    def __init__(self):
        super().__init__("OPEN FILE")
        # self.setStyleSheet(Config.INPUT_BTN)


class Window(QWidget):

    def __init__(self, type):
        super().__init__()
        self.__type = type
        self.Data = Data()
        self.__data = dict()
        self.__data["Data"] = ["1"] * self.Data.get_end_day()
        self.__plot = None
        self.__countries = []
        self.main_layout = QGridLayout()
        self.__prepare_window()

    def __prepare_window(self):
        self.__pdf_button = PDFButton(self)
        self.__slider_time = SliderWindow(100, self)
        self.__search = SearchPanel(self)
        self.__plot = Semilogy(self.__data, self.Data.get_start_day(), self.Data.get_end_day(), self)
        self.__country_box = CountryBox(self.__countries, self)
        self.__input = InputDataButton()
        self.__input.clicked.connect(self.input_click_func())
        self.__search.textChanged.connect(self.search_click_func())
        self.__reset_button = ResetButton(self)
        self.__mode_box = PlotBox(["Plot", "Semilogy"], self)

        self.main_layout.addWidget(self.__country_box, 1, 3, 3, 4)
        self.main_layout.addWidget(self.__plot, 0, 0, 4, 3)
        self.main_layout.addWidget(self.__pdf_button, 4, 4, 1, 1)
        self.main_layout.addWidget(self.__slider_time, 4, 0, 1, 3)
        self.main_layout.addWidget(self.__search, 0, 3, 1, 4)
        self.main_layout.addWidget(self.__input, 4, 3, 1, 1)
        self.main_layout.addWidget(self.__reset_button, 4, 5, 1, 1)
        self.main_layout.addWidget(self.__mode_box, 4, 6, 1, 1)
        self.main_layout.setContentsMargins(1, 1, 1, 1)

        self.setLayout(self.main_layout)

    def input_clicked(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Get Data File", "*.csv")
            if filename[0]:
                self.Data.set_filename(filename[0])

            EndDay(self.Data.get_filename(), self)
            FirstDay(self.Data.get_filename(), self)
            self.countries = ReadCountries(self.Data.get_filename()).get_countries()

            self.main_layout.removeWidget(self.__country_box)
            self.__country_box = CountryBox(self.countries, self)
            self.main_layout.addWidget(self.__country_box, 1, 3, 3, 4)

            data_range = ReadLen(self.Data.get_filename()).get_len()
            self.main_layout.removeWidget(self.__slider_time)
            self.__slider_time = SliderWindow(data_range, self)
            self.main_layout.addWidget(self.__slider_time, 4, 0, 1, 3)

            self.setLayout(self.main_layout)

        except:
            Warning("Brak pliku z danymi!")

    def input_click_func(self):
        return lambda _: self.input_clicked()

    def search_click_func(self):
        return lambda _: self.__search.search_clicked(self)

    def get_country_box(self):
        return self.__country_box

    def set_box(self, new):
        self.__country_box = new

    def get_slider(self):
        return self.__slider_time

    def get_graph(self):
        return self.__plot

    def get_type(self):
        return self.__type

    def get_reset(self):
        return self.__reset_button


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__tabs = QTabWidget()
        self.__tabs.addTab(Window("chorzy"), "Stwierdzone przypadki zachorowania")
        self.__tabs.addTab(Window("zdrowi"), "Ozdrowienia")
        self.setCentralWidget(self.__tabs)
        # self.setStyleSheet(Config.BACKGROUND_COLOR)
        self.setWindowTitle("Wirus.py")
        self.setFixedHeight(750)
        self.setFixedWidth(1200)

        self.centralWidget()
        icon = QIcon("juniwirus.png")
        self.setWindowIcon(icon)
        self.setIconSize(QSize(400, 400))
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle(Config.WINDOW_STYLE)
    window = MainWindow()

    sys.exit(app.exec_())

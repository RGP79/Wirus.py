import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, \
    QSlider, QLabel, QHBoxLayout, QFileDialog, QMainWindow, \
    QTabWidget
from PyQt5.QtGui import *
from panel.widgets import RangeSlider

from Graph import Graph
from Popup_windows import ErrorWindow

from datetime import datetime, timedelta

from Country_box import CountryBox
from Data import Data
from Graph import ReadCountries, ReadLen
from Graph_button import MakeGraphButton
from Pdf_button import PDFButton
from SearchPanel import SearchPanel

COUNTRY_COLUMN_ID = 1




class TimeSlider(QWidget):
    # implementacja suwaka do czasu

    def __init__(self, data_range):
        super().__init__()

        self.initUI(data_range)

    def initUI(self, data_range):
        hbox = QHBoxLayout()

        sld = QSlider(Qt.Horizontal, self)
        sld.setRange(0, data_range)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setPageStep(5)

        sld.valueChanged.connect(self.__update_label)

        self.label = QLabel('22-01-2020', self)
        Data.DAY = '22-01-2020'
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


class InputDataButton(QPushButton):
    def __init__(self):
        super().__init__("INPUT DATA")
        self.setStyleSheet("QPushButton"
                           "{"
                           "background-color : rgb(196,245,95);"
                           "}")


class Window(QWidget):
    # stworzenie okna i dodanie paneli do niego (wywoluje wszystkie klasy przyciskow itd)
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.data = dict()
        self.data["Data"] = ["1"] * 414
        self.__plot = None
        self.countries = ["Country_1", "Country_2", "Country_3", "Country_4", "Country_5"]
        self.main_layout = QGridLayout()
        self.__prepare_window()

    def __prepare_window(self):
        # self.countries = CountryBox.countries
        countries = ["Country_1", "Country_2", "Country_3", "Country_4", "Country_5"]
        self.__pdf_button = PDFButton()
        self.__slider_time = TimeSlider(100)
        self.__search = SearchPanel()
        self.__plot = Graph(self.data, Data.START_DAY, self.type)
        self.__country_box = CountryBox(countries)
        self.input = InputDataButton()
        self.input.clicked.connect(self.input_click_func())
        self.__graph_button = MakeGraphButton(self.type)
        self.__graph_button.clicked.connect(self.make_graph_click_func())
        self.__search.textChanged.connect(self.search_click_func())
        # stworzenie jakis widgetow (wywolanie fucnkji z gory)
        self.main_layout.addWidget(self.__country_box, 1, 3, 3, 2)
        self.main_layout.addWidget(self.__plot, 0, 0, 3, 3)
        self.main_layout.addWidget(self.__graph_button, 4, 0, 1, 1)
        self.main_layout.addWidget(self.__pdf_button, 4, 4, 1, 1)
        self.main_layout.addWidget(self.__slider_time, 4, 1, 1, 2)
        self.main_layout.addWidget(self.__search, 0, 3, 1, 2)
        self.main_layout.addWidget(self.input, 4, 3, 1, 1)
        # wsadzenie tych widgetow do okna (ustawinie pozycji)
        self.setLayout(self.main_layout)
        self.show()

    def input_click_func(self):
        return lambda _: self.input_clicked()

    def input_clicked(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Get Data File", "*.csv")
            Data.FILENAME = filename[0]
            # global COUNTRIES_CLICKED
            Data.COUNTRIES_CLICKED = []
            self.countries = ReadCountries(Data.FILENAME).get_countries()
            self.main_layout.removeWidget(self.__country_box)
            self.__country_box = CountryBox(self.countries)
            self.main_layout.addWidget(self.__country_box, 1, 3, 3, 2)
            self.setLayout(self.main_layout)
            data_range = ReadLen(Data.FILENAME).get_len()
            self.main_layout.removeWidget(self.__slider_time)
            self.__slider_time = TimeSlider(data_range)
            self.main_layout.addWidget(self.__slider_time, 4, 1, 1, 2)
            self.setLayout(self.main_layout)
            self.show()
        except:
            ErrorWindow("Nie Wybrano Pliku!")

    def make_graph_click_func(self):
        return lambda _: self.__graph_button.graph_clicked(self)

    def search_click_func(self):
        return lambda _: self.__search.search_clicked(self)

    def get_country_box(self):
        return self.__country_box


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__tabs = QTabWidget()
        self.__tabs.addTab(Window("chorzy"), "Stwierdzone przypadki zachorowania")
        self.__tabs.addTab(Window("zdrowi"), "Ozdrowienia")
        self.setCentralWidget(self.__tabs)
        self.setStyleSheet("QWidget"
                           "{"
                           "background-color : lightblue;"
                           "}")
        self.setWindowTitle("WIRUS")
        self.setFixedHeight(900)
        self.setFixedWidth(1700)
        icon = QIcon()

        self.setWindowIcon(icon)
        self.setIconSize(QSize(400, 400))
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()

    sys.exit(app.exec_())

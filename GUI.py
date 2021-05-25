import sys
from enum import Enum, auto, unique

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QGroupBox, QPushButton, \
    QHBoxLayout, QSlider, QScrollArea, QFormLayout, QLabel, QHBoxLayout, QMessageBox, QFileDialog, QMainWindow, \
    QTabWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import *
from Graph import Graph
from Popup_windows import ErrorWindow

from datetime import datetime, timedelta

from Wirus.Country_box import PushCountryButtons, CountryBox
from Wirus.Data import Data
from Wirus.Graph import ReadCountries, ReadLen, ReadData
from Wirus.Graph_button import MakeGraphButton
from Wirus.SearchPanel import SearchPanel

COUNTRY_COLUMN_ID = 1


class PDFButton(QPushButton):
    # implementacja przycsiku do tworzenia pdf
    def __init__(self):
        super().__init__("EXPORT TO PDF")
        self.__value = "EXPORT TO PDF"
        self.clicked.connect(self.__PDF)
        self.setStyleSheet("QPushButton"
                           "{"
                           "background-color : rgb(196,245,95);"
                           "}")

    def __PDF(self):
        print("robie pdf")
        pass


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


class InputDataButton(QPushButton):
    def __init__(self):
        super().__init__("INPUT DATA")
        self.setStyleSheet("QPushButton"
                           "{"
                           "background-color : rgb(196,245,95);"
                           "}")


class Window(QWidget):
    # stworzenie okna i dodanie paneli do niego (wywoluje wszystkie klasy przyciskow itd)
    def __init__(self):
        super().__init__()
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
        self.__plot = Graph(self.data, Data.START_DAY)
        self.__country_box = CountryBox(countries)
        self.input = InputDataButton()
        self.input.clicked.connect(self.input_click_func())
        self.__graph_button = MakeGraphButton()
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
            print(data_range)
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

    def search_clicked(self):

        txt = self.__search.text()
        new = self.__search.get_btns(txt, self.countries)
        self.main_layout.removeWidget(self.__country_box)
        self.__country_box = CountryBox(new)
        self.main_layout.addWidget(self.__country_box, 1, 3, 3, 2)
        self.setLayout(self.main_layout)

    def get_country_box(self):
        return self.__country_box


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__tabs = QTabWidget()
        self.__tabs.addTab(Window(), "chorzy")
        self.__tabs.addTab(Window(), "zdrowi")
        self.setCentralWidget(self.__tabs)
        self.setStyleSheet("QWidget"
                           "{"
                           "background-color : lightblue;"
                           "}")
        self.setWindowTitle("WIRUS")
        self.setFixedHeight(900)
        self.setFixedWidth(1700)
        icon = QIcon()
        icon.addFile("lewap.png", QSize(100, 100))
        self.setWindowIcon(icon)
        self.setIconSize(QSize(400, 400))
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()

    sys.exit(app.exec_())

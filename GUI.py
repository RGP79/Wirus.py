import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, \
    QFileDialog, QMainWindow, QTabWidget
from PyQt5.QtGui import *
from Graph import Graph
from Exceptions import ErrorWindow
from Country_box import CountryBox
from Graph import ReadCountries, ReadLen
from Pdf_maker import PDFButton
from SearchPanel import SearchPanel
from Graph import FirstDay, EndDay
from TimeSlider import SliderWindow
from ResetButton import ResetButton
from Data import Data
from Wirus_git.Wirus_clone.Look_Config import Config

COUNTRY_COLUMN_ID = 1


class InputDataButton(QPushButton):
    def __init__(self):
        super().__init__("INPUT DATA")
        self.setStyleSheet(Config.INPUT_BTN)


class Window(QWidget):
    # stworzenie okna i dodanie paneli do niego (wywoluje wszystkie klasy przyciskow itd)

    def __init__(self, type, data):
        super().__init__()
        self.type = type
        self.Data = data
        self.data = dict()
        self.data["Data"] = ["1"] * 414
        self.__plot = None
        self.countries = []
        self.main_layout = QGridLayout()
        self.__prepare_window()

    def __prepare_window(self):
        self.__pdf_button = PDFButton(self)
        self.__slider_time = SliderWindow(100, self)
        self.__search = SearchPanel(self)
        self.__plot = Graph(self.data, self.Data.START_DAY, self.Data.END_DAY, self)
        self.__country_box = CountryBox(self.countries, self)
        self.input = InputDataButton()
        self.input.clicked.connect(self.input_click_func())
        self.__search.textChanged.connect(self.search_click_func())
        self.__reset_button = ResetButton(self)

        # stworzenie jakis widgetow (wywolanie fucnkji z gory)
        self.main_layout.addWidget(self.__country_box, 1, 3, 3, 3)
        self.main_layout.addWidget(self.__plot, 0, 0, 4, 3)
        self.main_layout.addWidget(self.__pdf_button, 4, 4, 1, 1)
        self.main_layout.addWidget(self.__slider_time, 4, 0, 1, 3)
        self.main_layout.addWidget(self.__search, 0, 3, 1, 3)
        self.main_layout.addWidget(self.input, 4, 3, 1, 1)
        self.main_layout.addWidget(self.__reset_button, 4, 5, 1, 1)
        self.main_layout.setContentsMargins(1, 1, 1, 1)

        # wsadzenie tych widgetow do okna (ustawinie pozycji)
        self.setLayout(self.main_layout)

    def input_clicked(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Get Data File", "*.csv")
            if filename[0]:
                self.Data.FILENAME = filename[0]
            print(filename[0])
            EndDay(self.Data.FILENAME, self)
            FirstDay(self.Data.FILENAME, self)
            self.countries = ReadCountries(self.Data.FILENAME).get_countries()
            print(self.countries)
            self.main_layout.removeWidget(self.__country_box)
            self.__country_box = CountryBox(self.countries, self)
            self.main_layout.addWidget(self.__country_box, 1, 3, 3, 3)
            print("2")
            data_range = ReadLen(self.Data.FILENAME).get_len()
            self.main_layout.removeWidget(self.__slider_time)
            self.__slider_time = SliderWindow(data_range, self)
            self.main_layout.addWidget(self.__slider_time, 4, 0, 1, 3)

            self.setLayout(self.main_layout)

        except:
            ErrorWindow("Brak pliku z danymi!")
        print(self.Data.FILENAME)

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
        return self.type


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__tabs = QTabWidget()
        self.__tabs.addTab(Window("chorzy", Data()), "Stwierdzone przypadki zachorowania")
        self.__tabs.addTab(Window("zdrowi", Data()), "Ozdrowienia")
        self.setCentralWidget(self.__tabs)
        self.setStyleSheet(Config.BACKGROUND_COLOR)
        self.setWindowTitle("WIRUS")
        self.setFixedHeight(750)
        self.setFixedWidth(1075)

        # self.isMaximized()
        self.centralWidget()
        icon = QIcon("lewap.png")
        self.setWindowIcon(icon)
        self.setIconSize(QSize(400, 400))
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle(Config.WINDOW_STYLE)
    window = MainWindow()

    sys.exit(app.exec_())

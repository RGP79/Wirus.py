import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, \
    QFileDialog, QMainWindow, QTabWidget
from PyQt5.QtGui import *
from Graph import Graph
from Exceptions import ErrorWindow
from Country_box import CountryBox
from Data import Data
from Graph import ReadCountries, ReadLen
from Pdf_maker import PDFButton
from SearchPanel import SearchPanel
from TimeSlider import TimeSlider

COUNTRY_COLUMN_ID = 1


class InputDataButton(QPushButton):
    def __init__(self):
        super().__init__("INPUT DATA")
        self.setStyleSheet("QPushButton"
                           "{"
                           "background-color : rgb(97,150,85);"
                           "}")


class Window(QWidget):
    # stworzenie okna i dodanie paneli do niego (wywoluje wszystkie klasy przyciskow itd)
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.data = dict()
        self.data["Data"] = ["1"] * 414
        self.__plot = None
        self.countries = []
        self.main_layout = QGridLayout()
        self.__prepare_window()

    def __prepare_window(self):
        self.__pdf_button = PDFButton()
        self.__slider_time = TimeSlider(100, self, self.type)
        self.__search = SearchPanel(self, self.type)
        self.__plot = Graph(self.data, Data.START_DAY, self.type)
        self.__country_box = CountryBox(self.countries, self, self.type)
        self.input = InputDataButton()
        self.input.clicked.connect(self.input_click_func())
        self.__search.textChanged.connect(self.search_click_func())

        # stworzenie jakis widgetow (wywolanie fucnkji z gory)
        self.main_layout.addWidget(self.__country_box, 1, 3, 3, 2)
        self.main_layout.addWidget(self.__plot, 0, 0, 3, 3)
        self.main_layout.addWidget(self.__pdf_button, 4, 4, 1, 1)
        self.main_layout.addWidget(self.__slider_time, 4, 0, 1, 3)
        self.main_layout.addWidget(self.__search, 0, 3, 1, 2)
        self.main_layout.addWidget(self.input, 4, 3, 1, 1)

        # wsadzenie tych widgetow do okna (ustawinie pozycji)
        self.setLayout(self.main_layout)
        self.show()

    def input_clicked(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Get Data File", "*.csv")
            Data.FILENAME = filename[0]
            # print(filename[0])

            self.countries = ReadCountries(Data.FILENAME).get_countries()
            self.main_layout.removeWidget(self.__country_box)
            self.__country_box = CountryBox(self.countries, self, self.type)
            self.main_layout.addWidget(self.__country_box, 1, 3, 3, 2)

            data_range = ReadLen(Data.FILENAME).get_len()
            self.main_layout.removeWidget(self.__slider_time)
            self.__slider_time = TimeSlider(data_range, self, self.type)
            self.main_layout.addWidget(self.__slider_time, 4, 0, 1, 3)

            self.setLayout(self.main_layout)
            self.show()
        except:
            ErrorWindow("Nie Wybrano Pliku!")

    def input_click_func(self):
        return lambda _: self.input_clicked()

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
                           "background-color : grey;"
                           "}")
        self.setWindowTitle("WIRUS")
        # self.setFixedHeight(750)
        # self.setFixedWidth(1075)
        # self.isMaximized()
        self.centralWidget()
        icon = QIcon("lewap.png")
        self.setWindowIcon(icon)
        self.setIconSize(QSize(400, 400))
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    # app.setStyle('Oxygen')
    window = MainWindow()

    sys.exit(app.exec_())

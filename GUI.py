import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QGroupBox, QPushButton, \
    QHBoxLayout, QSlider, QScrollArea, QFormLayout, QLabel, QHBoxLayout, QMessageBox, QFileDialog
from Graph import Graph, read_countries, read_countries_data, read_len
from Popup_windows import InputWindow, ErrorWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Figure
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime, timedelta

COUNTRY_COLUMN_ID = 1
COUNTRIES_CLICKED = []
FILENAME = None
START_DAY = 0
END_DAY = 100000


class PushCountryButtons(QPushButton):
    # implementacja wciskanego przycisku
    def __init__(self, name):
        super().__init__(name)
        self.__name = name
        self.ile = 0
        self.get_color()
        self.clicked.connect(self.func_print_me())

    def color(self):
        if self.ile == 1:
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : lightgreen;"
                               "}")
            self.ile = 0
        else:
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : red;"
                               "}")
            self.ile = 1

    def func_print_me(self):
        return lambda _: self.names()

    def names(self):
        print(self.__name)
        global COUNTRIES_CLICKED
        print(COUNTRIES_CLICKED)
        if self.ile == 1:
            name = self.__name
            COUNTRIES_CLICKED.remove(name)
        else:
            name = self.__name
            COUNTRIES_CLICKED.append(name)
        print("color")
        self.color()

        print(COUNTRIES_CLICKED)

    def get_color(self):
        if self.__name in COUNTRIES_CLICKED:
            self.ile = 1
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : red;"
                               "}")
        else:
            self.ile = 0
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : lightgreen;"
                               "}")


class PDFButton(QPushButton):
    # implementacja przycsiku do tworzenia pdf
    def __init__(self):
        super().__init__("EXPORT TO PDF")
        self.__value = "EXPORT TO PDF"
        self.clicked.connect(self.__PDF)
        self.setStyleSheet("QPushButton"
                           "{"
                           "background-color : lightgreen;"
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

        sld.valueChanged.connect(self.updateLabel)

        self.label = QLabel('22-01-2020', self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)

        hbox.addWidget(sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 350, 250)

    def updateLabel(self, value):
        date_format = '%d-%m-%Y'
        date = str(datetime.strptime('22-01-2020', date_format) + timedelta(value))
        self.label.setText(date[:10])
        global START_DAY
        START_DAY = int(value)


class InputDataButton(QPushButton):
    def __init__(self):
        super().__init__("INPUT DATA")
        self.setStyleSheet("QPushButton"
                           "{"
                           "background-color : lightgreen;"
                           "}")


class MakeGraphButton(QPushButton):
    # przycisk do tworzenia wykresu (prawdopodobnie sie usunie go)
    def __init__(self, parent: QWidget):
        super().__init__("MAKE GRAPH")
        self.__value = "MAKE GRAPH"
        self.setStyleSheet(("QPushButton"
                               "{"
                               "background-color : lightgreen;"
                               "}"))



class SearchPanel(QLineEdit):
    # implementajca wyszukiwarki panstw
    def __init__(self):
        super().__init__()

        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)

    def get_btns(self, txt, countries):
        new = []
        for ctn in countries:
            if txt.upper() == ctn.upper()[0:len(txt)]:
                new.append(ctn)
        return new


class CountryBox(QScrollArea):
    # implementacja panelu z krajami (stworzenie boxa + przyciskow dla panstw)
    def __init__(self, countries):
        super().__init__()
        self.__n_of_countries = []
        self.__init_view(countries)
        self.all_countries = []


    def __init_view(self, countries):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()
        self.all_countries = countries
        for i in range(len(self.all_countries)):
            name = self.all_countries[i]
            btn = PushCountryButtons(name)  # tu trzeba zmienic na PushButton jak bedzie wiadomo jak kolorki
            # btn.clicked.connect((lambda name_to_show: lambda _: print(name_to_show))(name))
            btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setWidgetResizable(True)

    def countries(self):
        return len(self.__n_of_countries)

    def read_countries(self, filepath):
        countries = []
        with open(filepath, "r") as f:
            for line in f:
                countries = line.split("', '")
        return countries


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
        self.setStyleSheet("QWidget"
                           "{"
                           "background-color : lightblue;"
                           "}")
        self.setWindowTitle("WIRUS")
        self.setFixedHeight(900)
        self.setFixedWidth(1700)

    def data_upload(self, Input: InputDataButton):
        self.data = Input

    def xd2(self, Input: InputDataButton):
        return self.data_upload(Input)

    def __prepare_window(self):
        # self.countries = CountryBox.countries
        countries = ["Country_1", "Country_2", "Country_3", "Country_4", "Country_5"]
        self.setFixedWidth(1200)
        self.setFixedHeight(900)
        self.__pdf_button = PDFButton()
        self.__slider_time = TimeSlider(100)
        self.__search = SearchPanel()
        self.__plot = Graph(self.data, START_DAY)
        self.__country_box = CountryBox(countries)
        self.input = InputDataButton()
        self.input.clicked.connect(self.input_click_func())
        self.__graph_button = MakeGraphButton(self)
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
            print(f"{filename}")
            global FILENAME
            FILENAME = filename[0]
            self.countries = read_countries(filename[0])
            print(self.countries)
            self.main_layout.removeWidget(self.__country_box)
            self.__country_box = CountryBox(self.countries)
            self.main_layout.addWidget(self.__country_box, 1, 3, 3, 2)
            self.setLayout(self.main_layout)
            data_range = read_len(filename[0])
            self.main_layout.removeWidget(self.__slider_time)
            self.__slider_time = TimeSlider(data_range)
            self.main_layout.addWidget(self.__slider_time, 4, 1, 1, 2)
            self.setLayout(self.main_layout)
            self.show()
        except:
            ErrorWindow("Nie Wybrano Pliku!")

    def make_graph_click_func(self):
        return lambda _: self.graph_clicked()

    def graph_clicked(self):
        try:
            data = read_countries_data(FILENAME, COUNTRIES_CLICKED, START_DAY)
            print(data)
            self.__plot = Graph(data, START_DAY)
            self.main_layout.addWidget(self.__plot, 0, 0, 3, 3)
            self.setLayout(self.main_layout)
            self.show()
        except:
            ErrorWindow("Nie wybrano Pliku lub Państw!")

    def search_click_func(self):
        return lambda _: self.search_clicked()

    def search_clicked(self):

        txt = self.__search.text()
        new = self.__search.get_btns(txt, self.countries)

        self.main_layout.removeWidget(self.__country_box)
        self.__country_box = CountryBox(new)
        self.main_layout.addWidget(self.__country_box, 1, 3, 3, 2)
        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QApplication([])

    window = Window()

    sys.exit(app.exec_())

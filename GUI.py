import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QGroupBox, QPushButton, \
    QHBoxLayout, QSlider, QScrollArea, QFormLayout, QLabel, QHBoxLayout, QMessageBox, QFileDialog
from Graph import Graph, read_countries, read_countries_data
from Popup_windows import InputWindow, ErrorWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Figure
from matplotlib import pyplot as plt
import numpy as np

COUNTRY_COLUMN_ID = 1
COUNTRIES_CLICKED = []
FILENAME = None


class PushCountryButtons(QPushButton):
    # implementacja wciskanego przycisku
    def __init__(self):
        super().__init__()
        self.ile = 0


class PDFButton(QPushButton):
    # implementacja przycsiku do tworzenia pdf
    def __init__(self):
        super().__init__("EXPORT TO PDF")
        self.__value = "EXPORT TO PDF"
        self.clicked.connect(self.__PDF)

    def __PDF(self):
        print("robie pdf")
        pass


class TimeSlider(QWidget):
    # implementacja suwaka do czasu

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        sld = QSlider(Qt.Horizontal, self)
        sld.setRange(0, 100)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setPageStep(5)

        sld.valueChanged.connect(self.updateLabel)

        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)

        hbox.addWidget(sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 350, 250)

    def updateLabel(self, value):
        self.label.setText(str(value))


class InputDataButton(QPushButton):
    def __init__(self):
        super().__init__("INPUT DATA")
        self.countries = "Poland"
        self.filepath = None
        self.__value = "INPUT DATA"
        self.data = None


class MakeGraphButton(QPushButton):
    # przycisk do tworzenia wykresu (prawdopodobnie sie usunie go)
    def __init__(self, parent: QWidget):
        super().__init__("MAKE GRAPH")
        self.__value = "MAKE GRAPH"

    def __graph(self, lol):
        return lambda _: print(lol)


class SearchPanel(QLineEdit):
    # implementajca wyszukiwarki panstw
    def __init__(self):
        super().__init__()

        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200, 32)
        pybutton.move(80, 60)

    def clickMethod(self):
        print('Your name: ' + self.line.text())

    pass


class CountryBox(QScrollArea):
    # implementacja panelu z krajami (stworzenie boxa + przyciskow dla panstw)
    def __init__(self, countries):
        super().__init__()
        self.__n_of_countries = []
        self.__init_view(countries)
        self.pushed = []
        self.all_countries = []

    def __init_view(self, countries):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()
        self.all_countries = countries
        for i in range(len(self.all_countries)):
            name = self.all_countries[i]
            btn = QPushButton(name)  # tu trzeba zmienic na PushButton jak bedzie wiadomo jak kolorki
            btn.setStyleSheet("QPushButton"
                              "{"
                              "background-color : lightblue;"
                              "}"
                              "QPushButton::pressed"
                              "{"
                              "background-color : red;"
                              "}"
                              )
            # btn.clicked.connect((lambda name_to_show: lambda _: print(name_to_show))(name))
            btn.clicked.connect(self.func_print_me(name))
            btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setWidgetResizable(True)

    def func_print_me(self, name):
        return lambda _: self.names(name)

    def names(self, name):

        self.pushed.append(name)
        print(self.pushed)
        global COUNTRIES_CLICKED
        COUNTRIES_CLICKED.append(name)

    def countries(self):
        return len(self.__n_of_countries)

    def read_countries(self, filepath):
        countries = []
        with open(filepath, "r") as f:
            for line in f:
                countries = line.split("', '")
        return countries


class Plot(Figure):
    def __init__(self):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)
        self.new()

    def new(self):
        t = np.arange(0.0, 2.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.ax.plot(t, s)


class Window(QWidget):
    # stworzenie okna i dodanie paneli do niego (wywoluje wszystkie klasy przyciskow itd)
    def __init__(self):
        super().__init__()
        self.data = dict()
        self.__country_box = None
        self.__plot = None
        self.main_layout = QGridLayout()
        self.__prepare_window()

    def data_upload(self, Input: InputDataButton):
        self.data = Input

    def xd2(self, Input: InputDataButton):
        return self.data_upload(Input)

    def __prepare_window(self):
        # self.countries = CountryBox.countries
        self.setFixedWidth(1200)
        self.setFixedHeight(900)
        self.__pdf_button = PDFButton()
        self.__slider_time = TimeSlider()
        self.__search = SearchPanel()
        self.input = InputDataButton()
        self.input.clicked.connect(self.input_click_func())
        self.__graph_button = MakeGraphButton(self)
        self.__graph_button.clicked.connect(self.make_graph_click_func())
        # stworzenie jakis widgetow (wywolanie fucnkji z gory)
        self.main_layout.addWidget(self.__country_box, 1, 4, 3, 1)
        self.main_layout.addWidget(self.__plot, 0, 0, 3, 3)
        self.main_layout.addWidget(self.__graph_button, 4, 0, 1, 1)
        self.main_layout.addWidget(self.__pdf_button, 4, 4, 1, 1)
        self.main_layout.addWidget(self.__slider_time, 4, 1, 1, 2)
        self.main_layout.addWidget(self.__search, 0, 4, 1, 2)
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
            countries = read_countries(filename[0])
            print(countries)
            if self.__country_box == None:
                self.__country_box = CountryBox(countries)
            self.main_layout.addWidget(self.__country_box, 1, 4, 3, 1)
            self.setLayout(self.main_layout)
            self.show()
        except:
            ErrorWindow("Nie Wybrano Pliku!")

    def make_graph_click_func(self):
        return lambda _: self.graph_clicked()

    def graph_clicked(self):
        try:
            data = read_countries_data(FILENAME, COUNTRIES_CLICKED)
            print(data)
            self.__plot = Graph(data)
            self.main_layout.addWidget(self.__plot, 0, 0, 3, 3)
            self.setLayout(self.main_layout)
            self.show()
        except:
            ErrorWindow("Nie wybrano Pliku lub Państw!")


if __name__ == "__main__":
    app = QApplication([])

    window = Window()

    sys.exit(app.exec_())

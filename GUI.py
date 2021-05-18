import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QGroupBox, QPushButton, \
    QHBoxLayout, QSlider, QScrollArea, QFormLayout, QLabel, QHBoxLayout, QSizePolicy, QMessageBox, QFileDialog
from Graph import Graph
from Popup_windows import InputWindow, ErrorWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
from matplotlib import pyplot as plt
import numpy as np

COUNTRY_COLUMN_ID = 1
data = dict()


class PushCountryButtons(QPushButton):
    # implementacja wciskanego przycisku
    pass


class PDFButton(QPushButton):
    # implementacja przycsiku do tworzenia pdf
    def __init__(self):
        super().__init__("EXPORT TO PDF")
        self.__value = "EXPORT TO PDF"
        self.clicked.connect(self.__PDF)

    def __PDF(self):
        print(window.countries)
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
        self.clicked.connect(self.xd)
        self.data = None

    def xd(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Get Data File", "*.csv")
            print(f"{filename}")
            self.__input(filename[0])
        except:
            ErrorWindow("Nie Wybrano Pliku!")

    def __input(self, filename):
        print("input")  # wywolanie classy/metody z okienkiem do inputu
        self.data = self.read_countries_data(filename, self.countries)
        print(self.data)
        global data
        data = self.data
        print(data)

        # Plot.new([1, 2, 3, 4, 5, 6], xdd)

    def get_patients_as_vector(self, country_data_line):
        n_of_unimportant_column = 4
        if country_data_line[0:2] == ',"':
            n_of_unimportant_column = 5
        n_of_patients_in_time = country_data_line.split(",")[n_of_unimportant_column:]
        n_of_patients_in_time = [int(val) for val in n_of_patients_in_time]

        return n_of_patients_in_time

    def read_countries_data(self, filepath, countries):
        countries_data = dict()

        with open(filepath, "r") as f:
            for line in f:
                if line[0] == ",":
                    maybe_country = line.split(",")[COUNTRY_COLUMN_ID]
                    if maybe_country in countries:
                        line = line.strip()
                        n_of_patients_in_time = self.get_patients_as_vector(line)
                        countries_data[maybe_country] = n_of_patients_in_time
        return countries_data

    def get_countries(self):
        return self.countries

    def get_data(self):
        return self.data


class MakeGraphButton(QPushButton):
    # przycisk do tworzenia wykresu (prawdopodobnie sie usunie go)
    def __init__(self, parent: QWidget):
        super().__init__("MAKE GRAPH")
        self.__value = "MAKE GRAPH"
        self.__data = dict()
        self.clicked.connect(self.__graph)

    def __graph(self):
        self.__data = data
        global graph
        graph = Graph(self.__data)
        chuj = Window()
        # graph.show()
        chuj.update_window_plot()

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
    def __init__(self, size):
        super().__init__()
        self.__n_of_countries = []
        self.__init_view(size)
        self.pushed = []

    def __init_view(self, size):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        for i in range(size):
            name = f"btn{i}"
            btn = QPushButton(name)  # tu trzeba zmienic na PushButton jak bedzie wiadomo jak kolorki
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

    def countries(self):
        return len(self.__n_of_countries)


class Plot(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.draw()
        # self.plot()

    def plot(self):
        data = [random.random() for i in range(50)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

    # def create_graph(self):
    #     self.plot()



class Window(QWidget):
    # stworzenie okna i dodanie paneli do niego (wywoluje wszystkie klasy przyciskow itd)
    def __init__(self):
        super().__init__()
        self.data = dict()
        self.__prepare_window()

    def data_upload(self, Input: InputDataButton):
        self.data = Input

    def xd2(self, Input: InputDataButton):
        return self.data_upload(Input)

    def __prepare_window(self):
        # self.countries = CountryBox.countries
        self.__country_box = CountryBox(12)
        self.__pdf_button = PDFButton
        self.__slider_time = TimeSlider()
        self.__search = SearchPanel()
        self.__plot = Plot()
        self.input = InputDataButton()
        self.__graph_button = MakeGraphButton(self)
        # stworzenie jakis widgetow (wywolanie fucnkji z gory)
        main_layout = QGridLayout()
        main_layout.addWidget(self.__country_box, 1, 4, 3, 1)
        main_layout.addWidget(self.__plot, 0, 0, 3, 3)
        main_layout.addWidget(self.__graph_button, 4, 0, 1, 1)
        # main_layout.addWidget(self.__pdf_button, 4, 4, 1, 1)
        main_layout.addWidget(self.__slider_time, 4, 1, 1, 2)
        main_layout.addWidget(self.__search, 0, 4, 1, 2)
        main_layout.addWidget(self.input, 4, 3, 1, 1)
        # wsadzenie tych widgetow do okna (ustawinie pozycji)
        self.setLayout(main_layout)
        self.show()

    def update_window_plot(self):
        lol = Plot()
        self.__plot = lol.plot()
        self.repaint()
        print("lol")

        # main_layout = QGridLayout()
        # main_layout.addWidget(self.__plot, 0, 0, 3, 3)

    def input_clicked(self):
        print("xd")


if __name__ == "__main__":
    app = QApplication([])

    window = Window()

    sys.exit(app.exec_())

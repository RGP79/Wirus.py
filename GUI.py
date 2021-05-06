import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QGroupBox, QPushButton, \
    QHBoxLayout, QSlider, QScrollArea, QFormLayout, QLabel, QHBoxLayout, QMessageBox
from Graph import Graph
from Popup_windows import InputWindow

COUNTRY_COLUMN_ID = 1


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
        self.countries = "Poland,Germany"
        self.filepath = "covid.csv"
        self.__value = "INPUT DATA"
        self.clicked.connect(self.xd)
        self.__data = dict()

    def xd(self):
        return self.__input()

    def __input(self):
        print("input")  # wywolanie classy/metody z okienkiem do inputu
        self.__data = self.read_countries_data(self.filepath, self.countries)
        print(self.__data)

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

                    line = line.strip()
                    n_of_patients_in_time = self.get_patients_as_vector(line)
                    countries_data[maybe_country] = n_of_patients_in_time
        return countries_data

    def get_countries(self):
        return self.countries

    def get_data(self):
        return self.__data


class MakeGraphButton(QPushButton):
    # przycisk do tworzenia wykresu (prawdopodobnie sie usunie go)
    def __init__(self, lol):
        super().__init__("MAKE GRAPH")
        self.__lol = lol
        self.__value = "MAKE GRAPH"
        self.clicked.connect(self.__graph(lol))

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
    def __init__(self, size):
        super().__init__()
        self.__n_of_countries = []
        self.__init_view(size)

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
        return lambda _: print(name)

    def countries(self):
        return len(self.__n_of_countries)


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
        self.__input = InputDataButton()
        self.__input.clicked.connect(self.xd2(self.__input))
        self.__graph_button = MakeGraphButton(self.data)
        # lol = self.__input
        # stworzenie jakis widgetow (wywolanie fucnkji z gory)
        main_layout = QGridLayout()
        main_layout.addWidget(self.__country_box, 1, 4, 3, 1)
        main_layout.addWidget(self.__graph_button, 4, 0, 1, 1)
        # main_layout.addWidget(self.__pdf_button, 4, 4, 1, 1)
        main_layout.addWidget(self.__slider_time, 4, 1, 1, 2)
        main_layout.addWidget(self.__search, 0, 4, 1, 2)
        main_layout.addWidget(self.__input, 4, 3, 1, 1)
        # wsadzenie tych widgetow do okna (ustawinie pozycji)
        self.setLayout(main_layout)
        self.show()


if __name__ == "__main__":
    app = QApplication([])

    window = Window()

    sys.exit(app.exec_())

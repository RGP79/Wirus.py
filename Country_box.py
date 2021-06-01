from enum import Enum, auto, unique
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QScrollArea, QFormLayout, QGroupBox, QGraphicsDropShadowEffect, QPushButton
from Data import Data
from Graph import make_graph
from Exceptions import ErrorWindow


@unique
class Color(Enum):
    NOT_CLICKED = auto()
    CLICKED = auto()


class CountryBox(QScrollArea):
    # implementacja panelu z krajami (stworzenie boxa + przyciskow dla panstw)
    def __init__(self, countries, parent, type):
        super().__init__()
        self.type = type
        self.verticalScrollBar().setDisabled(False)
        self.parent = parent
        self.__n_of_countries = []
        self.__init_view(countries)
        self.all_countries = []


    def __init_view(self, countries):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()
        self.all_countries = countries
        for i in range(len(self.all_countries)):
            name = self.all_countries[i]
            btn = PushCountryButtons(name, self.parent,
                                     self.type)  # tu trzeba zmienic na PushButton jak bedzie wiadomo jak kolorki
            btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setWidgetResizable(True)


class PushCountryButtons(QPushButton):
    def __init__(self, name, parent, type):
        super().__init__(name)
        self.__name = name
        self.type = type
        self.parent = parent
        self.mode = Color.NOT_CLICKED
        self.get_color()
        self.clicked.connect(self.func_click_me())
        self.setFont(QFont("Helvetica", 10))
        # self.shadow = QGraphicsDropShadowEffect()
        # self.shadow.setBlurRadius(5)
        # self.shadow.setXOffset(3)
        # self.shadow.setYOffset(3)
        # self.setGraphicsEffect(self.shadow)

    def color(self):
        if self.mode == Color.CLICKED:
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : lightblue;"
                               "}")
            self.mode = Color.NOT_CLICKED
        else:
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : lightblue;"
                               "}")
            self.mode = Color.CLICKED

    def func_click_me(self):
        return lambda _: self.names()

    def names(self):

        if self.mode == Color.CLICKED:
            name = self.__name
            Data.COUNTRIES_CLICKED.remove(name)
            self.color()
            make_graph(self.type, self.parent)
        else:
            if len(Data.COUNTRIES_CLICKED) < 6:
                name = self.__name
                Data.COUNTRIES_CLICKED.append(name)
                self.get_color()
                make_graph(self.type, self.parent)
            else:
                ErrorWindow("Mozna dodac maksymalnie 6 krajow!")
        print(Data.COUNTRIES_CLICKED)

    def get_color(self):
        if self.__name in Data.COUNTRIES_CLICKED:
            self.mode = Color.CLICKED
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : rgb(97,150,85);"
                               "}")
        else:
            self.mode = Color.NOT_CLICKED
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : lightblue;"
                               "}")

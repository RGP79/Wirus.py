from enum import Enum, auto, unique

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QScrollArea, QFormLayout, QGroupBox, QGraphicsDropShadowEffect, QPushButton

from Wirus.Data import Data
from Wirus.Graph import ReadData, Graph

from Wirus.Popup_windows import ErrorWindow


@unique
class Color(Enum):
    NOT_CLICKED = auto()
    CLICKED = auto()


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

            btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setWidgetResizable(True)


class PushCountryButtons(QPushButton):
    # implementacja wciskanego przycisku
    def __init__(self, name):
        super().__init__(name)
        self.__name = name
        self.mode = Color.NOT_CLICKED
        self.get_color()
        self.clicked.connect(self.func_click_me())
        self.setFont(QFont("Arial Black", 10))
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setXOffset(3)
        self.shadow.setYOffset(3)
        self.setGraphicsEffect(self.shadow)

    def color(self):
        if self.mode == Color.CLICKED:
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : rgb(196,245,95);"
                               "}")
            self.mode = Color.NOT_CLICKED
        else:
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : rgb(67,220,133);"
                               "}")
            self.mode = Color.CLICKED

    def func_click_me(self):
        return lambda _: self.names()

    def names(self):

        if self.mode == Color.CLICKED:
            name = self.__name
            Data.COUNTRIES_CLICKED.remove(name)
            self.color()
        else:
            if len(Data.COUNTRIES_CLICKED) < 6:
                name = self.__name
                Data.COUNTRIES_CLICKED.append(name)
                self.get_color()
            else:
                ErrorWindow("Mozna dodac maksymalnie 6 krajow!")
        print(Data.COUNTRIES_CLICKED)
       #wywolanie klikniecia makegraph


    def get_color(self):
        if self.__name in Data.COUNTRIES_CLICKED:
            self.mode = Color.CLICKED
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : rgb(67,220,133);"
                               "}")
        else:
            self.mode = Color.NOT_CLICKED
            self.setStyleSheet("QPushButton"
                               "{"
                               "background-color : rgb(196,245,95);"
                               "}")

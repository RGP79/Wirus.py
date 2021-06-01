from PyQt5.QtWidgets import QPushButton
from Graph import make_graph
from Data import Data
from Exceptions import ErrorWindow



class ResetButton(QPushButton):
    def __init__(self, type, parent):
        self.__type = type
        self.__parent = parent
        super().__init__("RESET")
        self.__value = "RESET"
        # self.__pdf_generator = Reset()
        self.clicked.connect(self.__reset)
        self.setStyleSheet("QPushButton"
                           "{"
                           "background-color : rgb(97,150,85);"
                           "}")

    def __reset(self):
        try:
            Data.COUNTRIES_CLICKED = []
            for btn in self.__parent.get_country_box().all_buttons:
                btn.get_color()
            make_graph(self.__type, self.__parent)
            print(Data.COUNTRIES_CLICKED)
        except:
            ErrorWindow("Nie tedy drogsa")

# class Reset:
#     def __init__(self):

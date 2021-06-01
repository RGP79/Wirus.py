from PyQt5.QtWidgets import QPushButton
from Graph import make_graph

from Exceptions import ErrorWindow
from TimeSlider import update_sliders
from Wirus_git.Wirus_clone.Look_Config import Config


class ResetButton(QPushButton):
    def __init__(self, parent):
        self.__type = parent.get_type()
        self.__parent = parent
        super().__init__("RESET")
        self.__value = "RESET"
        # self.__pdf_generator = Reset()
        self.clicked.connect(self.__reset)
        self.setStyleSheet(Config.RESET_BTN)

    def __reset(self):
        try:
            self.__parent.Data.COUNTRIES_CLICKED = []
            for btn in self.__parent.get_country_box().all_buttons:
                btn.get_color()
            make_graph(self.__parent)
            update_sliders(self.__parent)
            print(self.__parent.Data.COUNTRIES_CLICKED)
        except:
            ErrorWindow("Nie tedy drogsa")

# class Reset:
#     def __init__(self):

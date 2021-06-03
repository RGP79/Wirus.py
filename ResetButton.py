from PyQt5.QtWidgets import QPushButton
from Graph import UpdateGraph
from Exceptions import ErrorWindow
from TimeSlider import UpdateSliders
from Look_Config import Config


class ResetButton(QPushButton):
    def __init__(self, parent):
        self.__type = parent.get_type()
        self.__parent = parent
        super().__init__("RESET")
        self.__value = "RESET"
        self.clicked.connect(self.reset)
        self.setStyleSheet(Config.RESET_BTN)

    def reset(self):
        try:
            self.__parent.Data.COUNTRIES_CLICKED = []
            for btn in self.__parent.get_country_box().all_buttons:
                btn.get_color()
            UpdateGraph(self.__parent)
            UpdateSliders(self.__parent)
            print(self.__parent.Data.COUNTRIES_CLICKED)
        except:
            ErrorWindow("Nie tedy drogsa")

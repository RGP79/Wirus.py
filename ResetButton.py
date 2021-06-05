from PyQt5.QtWidgets import QPushButton
from Graph import UpdateGraph
from TimeSlider import UpdateSliders
from Look_Config import Config


class ResetButton(QPushButton):
    def __init__(self, parent):

        self.__parent = parent
        super().__init__("RESET")
        self.clicked.connect(self.reset)
        self.setStyleSheet(Config.RESET_BTN)

    def reset(self):
        try:
            self.__parent.Data.reset_countries()
            for btn in self.__parent.get_country_box().all_buttons:
                btn.get_color()
            self.__parent.Data.set_end_pdf_date(self.__parent.Data.get_last_date())
            self.__parent.Data.set_start_pdf_date(self.__parent.Data.get_first_date())
            UpdateGraph(self.__parent)
            UpdateSliders(self.__parent)
        except:
            pass

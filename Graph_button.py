from PyQt5.QtWidgets import QPushButton, QWidget

from Graph import ReadData, Graph
from Popup_windows import ErrorWindow
from Wirus.Data import Data


class MakeGraphButton(QPushButton):
    # przycisk do tworzenia wykresu (prawdopodobnie sie usunie go)
    def __init__(self):
        super().__init__("MAKE GRAPH")
        self.__value = "MAKE GRAPH"
        self.setStyleSheet(("QPushButton"
                            "{"
                            "background-color : rgb(196,245,95);"
                            "}"))

    def graph_clicked(self, parent):
        try:
            data = ReadData(Data.FILENAME, Data.COUNTRIES_CLICKED, Data.START_DAY).get_data()
            plot = Graph(data, Data.START_DAY)
            print("jest plot")
            parent.main_layout.addWidget(plot, 0, 0, 3, 3)
            parent.setLayout(parent.main_layout)
            parent.show()
        except:
            ErrorWindow("Nie wybrano Pliku lub Państw!")

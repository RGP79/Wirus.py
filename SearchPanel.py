from PyQt5.QtWidgets import QLineEdit
from Country_box import CountryBox


class SearchPanel(QLineEdit):
    # implementajca wyszukiwarki panstw
    def __init__(self, parent, type):
        super().__init__()
        self.__parent = parent
        self.__type = type
        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.setStyleSheet(("QLineEdit"
                            "{"
                            "background-color : lightblue;"
                            "}"))

    def get_btns(self, txt, countries):
        new = []
        for ctn in countries:
            if txt.upper() == ctn.upper()[0:len(txt)]:
                new.append(ctn)
        return new

    def search_clicked(self, parent):

        txt = self.text()
        new = self.get_btns(txt, parent.countries)
        parent.main_layout.removeWidget(parent.get_country_box())
        new_box = CountryBox(new, self.__parent, self.__type)
        parent.main_layout.addWidget(new_box, 1, 3, 3, 3)
        parent.setLayout(parent.main_layout)

from enum import unique, Enum, auto

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox

from Wirus_git.Wirus_clone.Data import Data


class PlotBox(QWidget):
    def __init__(self, mode, parent):
        super().__init__()
        self.__mode = mode
        self.__parent = parent
        self.btns = []
        self.__init()

    def __init(self):
        layout = QVBoxLayout()
        for mode in self.__mode:
            chck = CheckBox(mode, self, self.__parent)
            layout.addWidget(chck)
        # self.btns[0].setChecked(True)
        self.setLayout(layout)


class CheckBox(QCheckBox):
    def __init__(self, name, box, parent):
        super().__init__(name)
        self.__name = name
        self.__parent = parent
        self.__box = box
        self.__init()

    def __init(self):
        self.__box.btns.append(self)
        if self.__name == "Semilogy":
            self.setChecked(True)
            self.setDisabled(True)
        self.stateChanged.connect(self.click)

    def click(self):
        return self.action()

    def action(self):
        if self.isChecked():
            self.__parent.Data.set_check_box(self.__name)
            for btn in self.__box.btns:
                if btn is not self:
                    btn.setChecked(False)
                    btn.setDisabled(False)
                    self.setDisabled(True)
            reset = self.__parent.get_reset()
            reset.reset()

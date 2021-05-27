from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


class ErrorWindow(QMessageBox):
    def __init__(self, msg):
        super().__init__()
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.setIcon(QMessageBox.Critical)
        icon = QIcon()
        self.setWindowIcon(icon)
        self.exec_()

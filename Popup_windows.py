from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


class ErrorWindow(QMessageBox):
    # okno do bledów
    def __init__(self, msg):
        # jakis konstruktor
        super().__init__()
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.setIcon(QMessageBox.Critical)
        icon = QIcon()
        icon.addFile("lewap.png", QSize(100, 100))
        self.setWindowIcon(icon)
        self.exec_()
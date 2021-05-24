
from PyQt5.QtWidgets import QMessageBox


class ErrorWindow(QMessageBox):
    # okno do bledów
    def __init__(self, msg):
        # jakis konstruktor
        super().__init__()
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.setIcon(QMessageBox.Critical)
        self.exec_()




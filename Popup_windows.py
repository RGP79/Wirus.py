import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QLineEdit, QPushButton


class ErrorWindow(QMessageBox):
    # okno do bledów
    def __init__(self, msg):
        # jakis konstruktor
        super().__init__()
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.setIcon(QMessageBox.Critical)
        self.exec_()


class InputWindow(QWidget):
    # okno do inputu
    def __init__(self):
        # jakis konstruktor

        super().__init__()
        self.setWindowTitle('Input Data')
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Infections input\n   filepath:')
        self.line = QLineEdit(self)
        self.line.move(100, 15)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        self.nameLabel1 = QLabel(self)
        self.nameLabel1.setText('Recovery input\n   filepath:')
        self.line1 = QLineEdit(self)
        self.line1.move(100, 60)
        self.line1.resize(200, 32)
        self.nameLabel1.move(20, 60)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200, 32)
        pybutton.move(100, 100)
        self.exec_()

    def clickMethod(self):
        print('Your name: ' + self.line.text())

        self.close()

        print('Your name2: ' + self.line1.text())

    def line(self):
        return self.line.text()


if __name__ == "__main__":
    app = QApplication([])

    window = InputWindow()
    sys.exit(app.exec_())

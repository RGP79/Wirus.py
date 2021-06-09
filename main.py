import sys

from PyQt5.QtWidgets import QApplication

from GUI import MainWindow
from Look_Config import Config

if __name__ == "__main__":
    print("xd_dziala_chyba")
    app = QApplication([])
    app.setStyle(Config.WINDOW_STYLE)
    window = MainWindow()

    sys.exit(app.exec_())

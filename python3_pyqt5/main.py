import sys

from PyQt5.QtWidgets import *

from mainwindow import MainWindow

import sip

if __name__ == "__main__":
    # app = QApplication(sys.argv)
    app = QApplication(["192.168.1.5"])
    w = MainWindow()
    w.show()
    # w.showMaximized()
    sys.exit(app.exec_())

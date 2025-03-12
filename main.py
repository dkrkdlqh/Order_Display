import sys

from PyQt5.QtWidgets import * 
from display.mainUI import MainUI


if __name__ == "__main__" : 
    app = QApplication(sys.argv)
    mainUI = MainUI()
    mainUI.show()
    sys.exit(app.exec_())
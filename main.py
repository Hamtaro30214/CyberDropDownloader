import sys
from PyQt5 import QtWidgets
from Controller import Controller


app = QtWidgets.QApplication(sys.argv)
controller = Controller()
controller.show_home_window()
sys.exit(app.exec_())

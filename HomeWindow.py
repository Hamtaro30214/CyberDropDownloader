import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.uic import loadUi
from DownloadFolder import DownloadFolder


class HomeWindow(QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(HomeWindow, self).__init__()
        loadUi("home_blueprint.ui", self)
        self.folder.clicked.connect(self.open_folder)
        self.url_button.clicked.connect(self.go_download_window)

    @staticmethod
    def open_folder(self):
        os.startfile(DownloadFolder())

    def go_download_window(self):
        if 'cyberdrop.me' in self.link.text():
            self.switch_window.emit(self.link.text())
        else:
            # consider option to allow link other than cyberdrop.me
            # warms user if link is invalid
            self.link.setStyleSheet("color: red;")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Invalid link!')
            msg.setInformativeText("Please try other link.")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

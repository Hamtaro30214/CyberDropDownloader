import os
from DownloadFolder import DownloadFolder
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QInputDialog
from ResizeButton import ResizeButton
from QHLine import QHLine


class HomeWindow(QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(HomeWindow, self).__init__()
        # title bar
        title = QLabel('CyberDropDownloader')
        title.setStyleSheet(
            'font-size: 18pt;'
            "color: #8be9fd;"
            'padding: 5px;'
        )

        # icons
        url_button = ResizeButton()
        url_button.setIcon(QtGui.QIcon('svg/external-link.svg'))
        url_button.clicked.connect(self.go_download_window)
        folder = ResizeButton()
        folder.setIcon(QtGui.QIcon('svg/folder.svg'))
        folder.clicked.connect(self.open_folder)

        # alignment
        vertical_layout = QVBoxLayout()
        horizontal_icons = QHBoxLayout()
        vertical_layout.addWidget(title)
        vertical_layout.addWidget(QHLine())
        horizontal_icons.addWidget(url_button)
        horizontal_icons.addWidget(folder)
        vertical_layout.addLayout(horizontal_icons)
        self.setStyleSheet('background-color:#383838;'
                           'padding:0;'
                           'margin:0;'
                           'color:#A9A9A9;')
        self.setLayout(vertical_layout)

    @staticmethod
    def open_folder(self):
        os.startfile(DownloadFolder())

    def go_download_window(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Type URl:')
        if ok and 'cyberdrop.me' in text:
            self.switch_window.emit(text)

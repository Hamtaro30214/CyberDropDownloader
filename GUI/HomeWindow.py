import os
import re
from DownloadFolder import DownloadFolder
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QInputDialog, QPushButton
from ResizeButton import ResizeButton
from QHLine import QHLine


class HomeWindow(QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(HomeWindow, self).__init__()
        self.setWindowTitle('Cyber Drop Downloader')

        # title bar
        title = QLabel('CyberDropDownloader')
        title.setStyleSheet(
            'font-size: 18pt;'
            "color: #8be9fd;"
            'padding: 5px;'
        )
        settings_button = QPushButton()
        settings_button.setIcon(QtGui.QIcon('svg/settings.svg'))
        settings_button.setStyleSheet('border: None')
        settings_button.setToolTip('<b>Change download folder</b>')
        settings_button.clicked.connect(self.change_download_folder)

        # icons
        url_button = ResizeButton()
        url_button.setIcon(QtGui.QIcon('svg/external-link.svg'))
        url_button.clicked.connect(self.go_download_window)
        url_button.setToolTip('<b>Input URL</b>')

        folder = ResizeButton()
        folder.setIcon(QtGui.QIcon('svg/folder.svg'))
        folder.setToolTip('<b>Open folder</b>')
        folder.clicked.connect(self.open_folder)

        # alignment
        vertical_layout = QVBoxLayout()
        horizontal_icons = QHBoxLayout()
        title_var = QHBoxLayout()
        title_var.addWidget(title, stretch=1)
        title_var.addWidget(settings_button)
        vertical_layout.addLayout(title_var)
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
            if not re.match('(?:http|https)://', text):
                text = 'https://{}'.format(text)
            self.switch_window.emit(text)

    def change_download_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        with open('config_files/download_path.txt', 'w') as f:
            f.write(folder_path)

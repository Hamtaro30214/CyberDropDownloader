import os
import pathlib
import bs4
import requests
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi


class HomeWindow(QDialog):
    def __init__(self):
        super(HomeWindow, self).__init__()
        loadUi("login.ui", self)
        self.folder.clicked.connect(self.open_folder)
        self.url_button.clicked.connect(self.go_download_window)
        self.download_path = self.create_folder()

    @staticmethod
    def create_folder():
        """
        Create download folder and return its path
        """
        download = str(pathlib.Path.home() / "Downloads")
        sub_folder = 'CyberDrop'
        download_path = os.path.join(download, sub_folder)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        return download_path

    def open_folder(self):
        os.startfile(self.download_path)

    def go_download_window(self):
        # add second window with image previews, now it allow to download images from user input in GUI
        if 'cyberdrop.me' in self.link.text():
            self.download_images()
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

    def save_image(self, image_link: str):
        """
        Creates the full path with the filename and saves each image to download_folder.
        """
        full_path = f'{self.download_path}/{image_link.split("/")[-1]}'
        image = requests.get(image_link).content
        with open(full_path, 'wb') as final_image:
            final_image.write(image)
        return f"Saved to: {full_path}"

    def download_images(self):
        # get list of urls to images
        htmldata = requests.get(self.link.text())
        soup = bs4.BeautifulSoup(htmldata.text, 'html.parser')
        lq_images = [item['src'] for item in soup.find_all('img')]
        hq_images = [i['data-src'] for i in soup.find_all("a", {"class": "image"})]
        # download each image and save it to folder
        for img in lq_images[1:-1]:
            print(self.save_image(img))

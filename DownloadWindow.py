import urllib
import bs4
import urllib.request
import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.uic import loadUi
from DownloadFolder import DownloadFolder


class DownloadWindow(QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self, link):
        self.link = link
        super(DownloadWindow, self).__init__()
        self.links = self.get_links_to_images(self.link)
        loadUi("download_blueprint.ui", self)
        self.back_button.clicked.connect(self.go_home_window)
        self.downlaod_button.clicked.connect(self.download_images)
        # scroll area
        h_box = QHBoxLayout()
        self.scrollAreaWidgetContents.setLayout(h_box)
        vertical_area = self.scrollAreaWidgetContents.layout()
        self.scrollArea.setWidgetResizable(True)
        images_len = len(self.links)
        self.label_img.setText(f'{images_len} images')
        while images_len > 0:
            images_len -= 3
            amount = 3
            if images_len < 0:
                amount += images_len
            print(images_len)
            vertical_area.addLayout(self.generate_photos(amount))

    def go_home_window(self):
        self.switch_window.emit()

    def generate_photos(self, amount=3):
        horizontal_photos = QHBoxLayout()
        for _ in range(amount):
            horizontal_photos.addWidget(self.preview_image())
        return horizontal_photos

    def preview_image(self):
        # preview image
        link = self.links[-1]
        self.links.pop()
        req = urllib.request.Request(link, headers={'User-Agent': "Magic Browser"})
        con = urllib.request.urlopen(req)

        # downloading image to variable
        pixmap = QPixmap()
        img = QLabel(self)
        pixmap.loadFromData(con.read())
        img.setPixmap(pixmap)
        return img

    @staticmethod
    def save_image(image_link: str):
        """
        Creates the full path with the filename and saves each image to download_folder.
        """
        full_path = f'{DownloadFolder()}/{image_link.split("/")[-1]}'
        image = requests.get(image_link).content
        with open(full_path, 'wb') as final_image:
            final_image.write(image)
        return f"Saved to: {full_path}"

    def download_images(self):
        for img in self.get_links_to_images(self.link):
            print(self.save_image(img))

    @staticmethod
    def get_links_to_images(link):
        # get list of urls to images
        htmldata = requests.get(link)
        soup = bs4.BeautifulSoup(htmldata.text, 'html.parser')
        # hq_images = [i['data-src'] for i in soup.find_all("a", {"class": "image"})]
        return [item['src'] for item in soup.find_all('img')][1:-1]

import math
import urllib
import bs4
import urllib.request
import requests
from urllib import request as url_req
from PIL import ImageFile
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.uic import loadUi
from CustomQFrame import CustomQFrame
from GUI.DownloadDialog import DownloadDialog


class DownloadWindow(QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self, link):
        super(DownloadWindow, self).__init__()
        self.link = link
        self.lq_images, self.hq_images = self.get_links_to_images()
        self.images_len = len(self.lq_images)
        self.image_list = []
        # GUI
        loadUi("download_blueprint.ui", self)
        self.back_button.setIcon(QIcon('svg/home.svg'))
        self.back_button.clicked.connect(self.go_home_window)
        self.label_img.setStyleSheet('color: #8be9fd;')
        self.label_img.setText(f'{self.images_len} images')
        self.label_img.setAlignment(QtCore.Qt.AlignRight)
        self.downlaod_button.setIcon(QIcon('svg/download.svg'))
        self.downlaod_button.clicked.connect(self.download_images)

        # scroll area
        self.scrollAreaWidgetContents.setLayout(QHBoxLayout())
        self.scrollArea.setWidgetResizable(True)
        vertical_area = self.scrollAreaWidgetContents.layout()

        # create images preview
        while self.images_len > 0:
            self.images_len -= 3
            amount = 3
            if self.images_len < 0:
                amount += self.images_len
            vertical_area.addLayout(self.generate_photos(amount))

    def generate_photos(self, amount):
        # generate up to 3 images horizontally
        horizontal_photos = QHBoxLayout()
        for _ in range(amount):
            lq_link = self.lq_images[-1]
            self.lq_images.pop()
            hq_link = self.hq_images[-1]
            self.hq_images.pop()

            # gui
            frame = CustomQFrame(hq_link)
            frame.image_miniature.setPixmap(self.preview_image(lq_link))
            bytes, (width, height) = self.get_sizes(hq_link)
            frame.image_size.setText(f"{bytes}, {width}x{height} px")

            horizontal_photos.addWidget(frame)
            self.image_list.append(frame)
        return horizontal_photos

    @staticmethod
    def preview_image(link):
        # preview image
        req = urllib.request.Request(link, headers={'User-Agent': "Magic Browser"})
        con = urllib.request.urlopen(req)

        # downloading image to variable
        pixmap = QPixmap()
        pixmap.loadFromData(con.read())
        return pixmap

    def get_links_to_images(self):
        # get list of urls to images
        htmldata = requests.get(self.link)
        soup = bs4.BeautifulSoup(htmldata.text, 'html.parser')
        lq_images = [item['src'] for item in soup.find_all('img')][1:-1]
        hq_images = [i['data-src'] for i in soup.find_all("a", {"class": "image"})]
        return lq_images, hq_images

    def go_home_window(self):
        self.switch_window.emit()

    def download_images(self):
        # open popup
        selected_images = [img.link for img in self.image_list if img.status]
        if selected_images:
            download_dialog = DownloadDialog(selected_images)
            download_dialog.exec()

    @staticmethod
    def get_sizes(url: str):
        def convert_size(size_bytes):
            if size_bytes == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return "%s %s" % (s, size_name[i])
        """
        Gets image size and file size in bytes without downloading the image.
        """
        file = url_req.urlopen(url)
        size = file.headers.get("content-length")
        if size:
            size = int(size)
        p = ImageFile.Parser()
        while True:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return convert_size(size), p.image.size
        # program might crash
        file.close()
        return size

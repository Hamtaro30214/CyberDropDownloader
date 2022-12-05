import bs4
import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.uic import loadUi
from CustomQFrame import CustomQFrame
from GUI.DownloadDialog import DownloadDialog
from QThreads.ImagePreview import ImagePreview


class DownloadWindow(QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self, link):
        super(DownloadWindow, self).__init__()
        self.link = link
        self.lq_images, self.hq_images = self.get_links_to_images()
        self.image_list = []

        # GUI
        loadUi("download_blueprint.ui", self)
        self.back_button.setIcon(QIcon('svg/home.svg'))
        self.back_button.clicked.connect(self.go_home_window)
        self.label_img.setStyleSheet('color: #8be9fd;')
        self.label_img.setText(f'{len(self.lq_images)} images')
        self.label_img.setAlignment(QtCore.Qt.AlignRight)
        self.downlaod_button.setIcon(QIcon('svg/download.svg'))
        self.downlaod_button.clicked.connect(self.download_images)

        # scroll area
        self.scrollAreaWidgetContents.setLayout(QHBoxLayout())
        self.scrollArea.setWidgetResizable(True)
        self.vertical_area = self.scrollAreaWidgetContents.layout()
        self.show()
        self.generate_preview()

    def generate_preview(self):
        self.horizontal_photos = QHBoxLayout()

        self.worker_thread = ImagePreview(self.lq_images, self.hq_images)
        self.worker_thread.setCurrentProgress.connect(self.update_progress)
        self.worker_thread.finished.connect(self.preview_finished)
        self.worker_thread.start()

    def update_progress(self, img, size, link):
        # generate up to 3 images horizontally
        if len(self.horizontal_photos) > 2:
            self.vertical_area.addLayout(self.horizontal_photos)
            self.horizontal_photos = QHBoxLayout()

        # create frame with img and size
        frame = CustomQFrame(link)
        frame.image_miniature.setPixmap(img)
        frame.image_size.setText(f"{size}")

        # add images to scroll area
        self.horizontal_photos.addWidget(frame)

        # add each frame to list of clickable images
        self.image_list.append(frame)

    def preview_finished(self):
        del self.worker_thread

        # add the remaining images to scroll area
        self.vertical_area.addLayout(self.horizontal_photos)

    def get_links_to_images(self) -> (str, str):
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

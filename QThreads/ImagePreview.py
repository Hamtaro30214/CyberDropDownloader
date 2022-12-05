import math
import urllib.request
from urllib import request as url_req
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap


class ImagePreview(QThread):
    setCurrentProgress = pyqtSignal(QPixmap, str, str)

    def __init__(self, lq_links, hq_links):
        super().__init__()
        self.lq_links = lq_links
        self.hq_links = hq_links

    def run(self):
        while self.lq_links:
            # create hq and lq link
            lq_link = self.lq_links[-1]
            self.lq_links.pop()
            hq_link = self.hq_links[-1]
            self.hq_links.pop()

            # return progress
            self.setCurrentProgress.emit(self.preview_image(lq_link), self.get_size(hq_link), hq_link)

    @staticmethod
    def preview_image(link: str) -> QPixmap:
        # preview image
        req = urllib.request.Request(link, headers={'User-Agent': "Magic Browser"})
        con = urllib.request.urlopen(req)

        # downloading image to variable
        pixmap = QPixmap()
        pixmap.loadFromData(con.read())
        return pixmap

    def get_size(self, link: str) -> str:
        # get size of file without downloading
        file = url_req.urlopen(link)
        size = file.headers.get("content-length")
        return self.convert_bytes(int(size))

    @staticmethod
    def convert_bytes(size_bytes: int) -> str:
        # convert bytes to more readable units
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

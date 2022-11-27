import sys
from urllib import request as url_req
from PIL import ImageFile
from PyQt5 import QtWidgets
from Controller import Controller


app = QtWidgets.QApplication(sys.argv)
controller = Controller()
controller.show_home_window()
sys.exit(app.exec_())


def get_sizes(url: str):
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
            return size, p.image.size
    file.close()
    return size

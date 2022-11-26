import sys
from urllib import request as url_req
from PIL import ImageFile
from PyQt5.QtWidgets import QApplication
from HomeWindow import HomeWindow
from PyQt5 import QtWidgets

app = QApplication(sys.argv)
main_window = HomeWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(main_window)
widget.resize(1280, 720)
widget.show()
app.exec_()


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

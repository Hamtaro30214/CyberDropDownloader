from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame


class CustomQFrame(QFrame):
    def __init__(self, link, parent=None):
        QFrame.__init__(self, parent)
        self.link = link
        self.status = False
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('color: #8be9fd')
        self.setLayout(self.layout)

    def mouseReleaseEvent(self, a0) -> None:
        if self.status:
            self.setStyleSheet('border: None; color: #8be9fd;')
        else:
            self.setStyleSheet('border: 1px solid gray; color: #8be9fd;')
        self.status = not self.status

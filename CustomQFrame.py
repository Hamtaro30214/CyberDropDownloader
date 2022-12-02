from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel


class CustomQFrame(QFrame):
    def __init__(self, link, parent=None):
        QFrame.__init__(self, parent)
        self.link = link
        self.status = False
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('color: #8be9fd; background-color: rgba(59,68,75, 90)')
        self.image_miniature = QLabel()
        self.image_miniature.setStyleSheet('border: None;')
        self.image_size = QLabel()
        self.image_size.setStyleSheet('border: None; color: #8be9fd; background-color: rgba(65,74,76,90);')
        self.layout.addWidget(self.image_miniature)
        self.layout.addWidget(self.image_size)
        self.setLayout(self.layout)

    def mouseReleaseEvent(self, a0) -> None:
        if self.status:
            self.setStyleSheet('border: None; background-color: rgba(59,68,75, 90)')
        else:
            self.setStyleSheet('border: 1px solid gray;')
        self.status = not self.status

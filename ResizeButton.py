from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QSizePolicy, QStyleOptionButton, QStyle
from PyQt5.QtWidgets import QPushButton


class ResizeButton(QPushButton):
    """
    auto resize button
    """
    def __init__(self, label=None, parent=None):
        super(ResizeButton, self).__init__(label, parent)
        self.pad = 4  # padding between the icon and the button frame
        self.minSize = 8  # minimum size of the icon
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet(
            '''QToolTip {
                background-color: #383838;
                color: #A9A9A9;
                border: #8ad4ff solid 1px;
            }'''
            '''QPushButton {
                background: #2c313c; 
                padding:0;
                margin:0;
            }'''
        )

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        # ---- get default style ----
        opt = QStyleOptionButton()
        self.initStyleOption(opt)

        # ---- scale icon to button size ----
        Rect = opt.rect
        h = Rect.height()
        w = Rect.width()
        iconSize = max(min(h, w) - 2 * self.pad, self.minSize)
        opt.iconSize = QtCore.QSize(iconSize, iconSize)
        # ---- draw button ----
        self.style().drawControl(QStyle.CE_PushButton, opt, qp, self)
        qp.end()

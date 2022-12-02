from PyQt5.QtWidgets import QFrame


class QHLine(QFrame):
    # create HLine from QT Designer
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

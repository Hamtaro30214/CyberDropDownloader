from GUI.HomeWindow import HomeWindow
from GUI.DownloadWindow import DownloadWindow


class Controller:
    def __init__(self):
        self.active_window = False

    def show_home_window(self):
        self.home = HomeWindow()
        self.home.switch_window.connect(self.show_download_window)
        self.home.resize(1280, 720)
        self.home.show()
        if self.active_window:
            self.download.close()

    def show_download_window(self, text):
        self.active_window = True
        self.download = DownloadWindow(text)
        self.download.switch_window.connect(self.show_home_window)
        self.download.resize(1280, 720)
        self.home.close()
        self.download.show()

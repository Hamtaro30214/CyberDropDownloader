from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QProgressBar
from QThreads.Downloader import Downloader


class DownloadDialog(QDialog):
    def __init__(self, links):
        super().__init__()
        self.links = links
        self.total = len(self.links)
        self.i = 0
        self.url = self.links[self.i]
        self.name = f'{self.links[self.i].split("/")[-1]}'
        self.download_status = True

        self.setWindowTitle("Download progress")
        self.label = QLabel("Press the button to start downloading.", self)
        self.label.setGeometry(20, 20, 200, 25)
        self.button = QPushButton("Start download", self)
        self.button.move(20, 40)
        self.button.pressed.connect(self.init_download)

        self.pause_resume_button = QPushButton("Pause", self)
        self.pause_resume_button.setGeometry(150, 40, 100, 30)
        self.pause_resume_button.pressed.connect(self.pause_resume)
        self.pause_resume_button.setEnabled(False)

        # number of download images
        self.downloaded_images = QLabel(f'Downloaded {self.i}/{self.total}', self)
        self.downloaded_images.setGeometry(20, 60, 300, 25)

        # progressBar for each successfully downloaded image
        self.mainBar = QProgressBar(self)
        self.mainBar.setGeometry(20, 80, 300, 25)
        self.mainBar.setValue(self.mainBar.minimum())

        # name of image
        self.image_name = QLabel(f'{self.name}', self)
        self.image_name.setGeometry(20, 100, 400, 25)

        # progressBar for each image
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(20, 120, 300, 25)
        self.progressBar.setValue(self.progressBar.minimum())
        self.show()

    def set_new_download(self):
        self.progressBar.setValue(self.progressBar.minimum())
        self.url = self.links[self.i]
        self.name = f'{self.links[self.i].split("/")[-1]}'
        self.image_name.setText(self.name)

    def update_downloaded_images(self):
        self.downloaded_images.setText(f'Downloaded {self.i}/{self.total}')

    def init_download(self):
        # Disable start button and enable pause/resume button
        self.button.setEnabled(False)
        self.pause_resume_button.setEnabled(True)
        # Run the download in a new thread.
        self.downloader = Downloader(self.url, self.name)
        # Connect the signals which send information about the download
        # progress with the proper methods of the progress bar.
        self.downloader.setTotalProgress.connect(self.progressBar.setMaximum)
        self.downloader.setCurrentProgress.connect(self.progressBar.setValue)
        # Qt will invoke the `succeeded()` method when the file has been
        # downloaded successfully and `downloadFinished()` when the child thread finishes.
        self.downloader.succeeded.connect(self.download_succeeded)
        self.downloader.finished.connect(self.download_finished)
        self.downloader.start()

    def download_succeeded(self):
        # Set the progress at 100%.
        self.progressBar.setValue(self.progressBar.maximum())

    def download_finished(self):
        # Delete the thread when no longer needed.
        del self.downloader
        self.i += 1
        self.mainBar.setValue(int(self.i / self.total * 100))
        self.update_downloaded_images()
        # checking for finished download
        if self.mainBar.value() == 100:
            self.progressBar.setValue(self.progressBar.maximum())
            self.download_status = False
            # Restore the buttons.
            self.button.setEnabled(True)
            self.pause_resume_button.setEnabled(False)
        # recreation of second download bar
        else:
            self.set_new_download()
            self.init_download()

    def pause_resume(self):
        # pause or resume downloading
        if self.pause_resume_button.text() == 'Pause':
            self.pause_resume_button.setText('Resume')
        else:
            self.pause_resume_button.setText('Pause')
        self.downloader.pause_resume()

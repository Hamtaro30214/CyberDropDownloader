import time
from urllib.request import urlopen
from PyQt5.QtCore import pyqtSignal, QThread
from DownloadFolder import DownloadFolder


class Downloader(QThread):
    # Signal for the window to establish the maximum value of the progress bar.
    setTotalProgress = pyqtSignal(int)
    # Signal to increase the progress.
    setCurrentProgress = pyqtSignal(int)
    # Signal to be emitted when the file has been downloaded successfully.
    succeeded = pyqtSignal()

    def __init__(self, url, filename):
        super().__init__()
        self.url = url
        self.filename = filename
        self.folder = DownloadFolder()
        self.is_paused = False

    def run(self):
        readBytes = 0
        chunkSize = 1024
        # Open the URL address
        with urlopen(self.url) as r:
            # Tell the window the amount of bytes to be downloaded.
            self.setTotalProgress.emit(int(r.info()["Content-Length"]))
            try:
                with open(f'{self.folder}/{self.filename}', "ab") as f:
                    while True:
                        # Read a piece of the file we are downloading.
                        chunk = r.read(chunkSize)
                        # If the result is `None`, that means data is not downloaded yet. Just keep waiting.
                        if chunk is None:
                            continue
                        # If the result is an empty `bytes` instance, then the file is complete.
                        elif chunk == b"":
                            break
                        # Write into the local file the downloaded chunk.
                        f.write(chunk)
                        readBytes += chunkSize
                        # Tell the window how many bytes we have received.
                        self.setCurrentProgress.emit(readBytes)

                        # pause downloading
                        while self.is_paused:
                            time.sleep(0)
            except Exception as e:
                # rework Exception!!!
                print('error img', e)
        # If this line is reached then no exception has occurred in the previous lines.
        self.succeeded.emit()

    def pause_resume(self):
        self.is_paused = not self.is_paused

import os
import pathlib


class DownloadFolder:
    def __new__(cls):
        download = str(pathlib.Path.home() / "Downloads")
        sub_folder = 'CyberDrop'
        download_path = os.path.join(download, sub_folder)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        return download_path


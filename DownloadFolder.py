import os
import pathlib


class DownloadFolder:
    """
    return path to download folder
    """
    def __new__(cls):
        if os.path.exists('config_files/download_path.txt'):
            # folder selected by user
            with open('config_files/download_path.txt', 'r') as f:
                download_path = f.readline()
        else:
            # default folder
            download = str(pathlib.Path.home() / "Downloads")
            sub_folder = 'CyberDrop'
            download_path = os.path.join(download, sub_folder)
            if not os.path.exists(download_path):
                os.makedirs(download_path)
        return download_path

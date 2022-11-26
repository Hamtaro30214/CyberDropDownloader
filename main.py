import requests
import bs4
import os
import pathlib
from urllib import request as url_req
from PIL import ImageFile


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


def save_image(download_folder: str, image_link: str):
    """
    Creates the full path with the filename and saves each image to download_folder.
    """
    full_path = f'{download_folder}/{image_link.split("/")[-1]}'
    image = requests.get(image_link).content
    with open(full_path, 'wb') as final_image:
        final_image.write(image)
    return f"Saved to: {full_path}"


# creating folder
download = str(pathlib.Path.home() / "Downloads")
sub_folder = 'CyberDrop'
download_path = os.path.join(download, sub_folder)
if not os.path.exists(download_path):
    os.makedirs(download_path)


# image scraping to list
htmldata = requests.get(input('Type link: '))
soup = bs4.BeautifulSoup(htmldata.text, 'html.parser')
lq_images = [item['src'] for item in soup.find_all('img')]
hq_images = [i['data-src'] for i in soup.find_all("a", {"class": "image"})]
for img in lq_images[1:-1]:
    print(save_image(download_path, img))

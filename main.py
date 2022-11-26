import requests
import bs4
import os
import pathlib


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
images = [item['src'] for item in soup.find_all('img')]
for img in images[1:-1]:
    print(save_image(download_path, img))

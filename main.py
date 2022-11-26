import requests
import bs4

htmldata = requests.get(input('Type link: '))
soup = bs4.BeautifulSoup(htmldata.text, 'html.parser')
images = [item['src'] for item in soup.find_all('img')]
for image in images:
    print(image)

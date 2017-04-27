from bs4 import BeautifulSoup
import requests

url = "www.sports-reference.com/cbb/schools/"

r = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data, "html.parser")

print(soup.get_text)

# for link in soup.find_all('a'):
#     print(link.get('href'))
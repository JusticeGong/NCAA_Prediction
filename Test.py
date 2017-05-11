from bs4 import BeautifulSoup
import requests
import re
import pickle

url = "www.sports-reference.com/cbb/schools/abilene-christian/2017-schedule.html"

r = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data, "html.parser")

# print(soup.get_text)

a = soup.find_all('tr')

print(a)
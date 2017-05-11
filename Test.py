from bs4 import BeautifulSoup
import requests
import re
import pickle

url = "www.sports-reference.com/cbb/schools/"

r = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data, "html.parser")

# for a in soup.find_all('tbody'):
#
#
# # print(soup.get_text)
#     print(a)

a = soup.find_all('td')
print(a[2])

# urlname = []
# schoolname = []
#
# a = soup.find_all(href=re.compile("/cbb/schools/*"))
#
# for i in range(2, 479):
#     # print("Found the URL:", a['href'].split('/')[3])
#     # print(a.contents)
#     urlname.append(a[i]['href'].split('/')[3])
#     schoolname = schoolname + a[i].contents



### Fina <a>
# a = soup.find_all(href=re.compile("/cbb/schools/*"))
# print(a)
#
# for i in range(1,len(a)):
#     print(a[i])
#     print('-----------------------' + str(i))
# ###
#
#
# for link in soup.find_all('a'):
#     print(link.get('href'))
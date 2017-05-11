from bs4 import BeautifulSoup
import requests
import re
import pickle

url = "www.sports-reference.com/cbb/schools/"

r = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data, "html.parser")

# print(soup.get_text)

urlname = []
schoolname = []

a = soup.find_all(href=re.compile("/cbb/schools/*"))

for i in range(2, 479):
    # print("Found the URL:", a['href'].split('/')[3])
    # print(a.contents)
    urlname.append(a[i]['href'].split('/')[3])
    schoolname = schoolname + a[i].contents
print(urlname)
print(schoolname)


with open('urlname.txt', 'w', encoding="utf8") as fu:
    fu.write(str(urlname))
fu.close()

with open('schoolname.txt', 'w', encoding="utf8") as fs:
    fs.write(str(schoolname))
fs.close()

# for i in range(1, len(schoolname)):
#     school = dict(str[schoolname[i]],str(urlname[i]))
#
# print(school)


### Fina <a>
# a = soup.find_all(href=re.compile("/cbb/schools/*"))
# print(a)
#
# for i in range(1,len(a)):
#     print(a[i].contents)
#     print('-----------------------' + str(i))
###


# for link in soup.find_all('a'):
#     print(link.get('href'))
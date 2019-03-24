import urllib.request
import time
from bs4 import BeautifulSoup
from selenium import webdriver


browser = webdriver.Chrome()
browser.get("https://ecos.fws.gov/ecp0/profile/speciesProfile?spcode=B08Z")
time.sleep(1)
html = browser.page_source
soup = BeautifulSoup(html, "lxml")
table = soup.find("table", {"id": "petitions-data-table"})
rows = table.find_all('tr')
tdData =[]
for row in rows:
 tds = row.find_all("td")
 tdData = [i.text for i in tds]
 print(tdData[0])
 

# for petetion in tdData:
 # string = petetion.split(",")
 # print("Petetion Ttitle")
 # print(string[0])
 # tdNum = 0
 # for td in tds:
  # if (tdNum ==0):
   # print("Petetion Ttitle")
   # print(td.text)
  # elif (tdNum ==1):
   # print("Petetion Received Date")
   # print(td.text)
  # tdNum +=1
# for link1 in soup.find_all('a'):
 # if ("county-modal") in str(link1.get('href')):
  # eventId = link1.get('href').split("-")[-1]
  # print(eventId)
browser.close()
browser.quit()

# content = urllib.request.urlopen("https://ecos.fws.gov/ecp0/profile/speciesProfile?spcode=B08Z")

# soup = BeautifulSoup(content, 'html.parser')

# table = soup.find('table', id="petitions-data-table")
# rows = table.findAll('tr')
# print(rows)
# for row in rows:
	# print(row)
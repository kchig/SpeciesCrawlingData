import sys
import collections
import urllib.request
import csv
import time
import json
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver


eventId = 0
sId = 0
baseURL = 'https://ecos.fws.gov/ecp0/profile/speciesProfile?spcode'


from os import listdir
from os.path import isfile, join
files = [f for f in listdir(str(sys.path[0])+"/data") if isfile(join(str(sys.path[0])+"/data", f))]

speciesFinal = open("SpeciesFinal.csv", "w")
speciesFinal.write("status, name, type, state, url,enlistedDate, counties, petetionDetails, spcode\n") 
filecounter = 0
for file in files:
	with open(str(sys.path[0])+"/data/"+file) as state_file:
		csv_reader = csv.reader(state_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count > 0:
				browser = webdriver.Chrome()
				browser.get(row[3])
				time.sleep(1)
				content = browser.page_source
				soup = BeautifulSoup(content, "lxml")
				content1 = urllib.request.urlopen(row[3]).read()
				soup1 = BeautifulSoup(content1, 'html.parser')
				imgURL=''
				for link in soup.find_all('a', attrs={'href': re.compile("/docs/species_images/")}):
				 imgURL="https://ecos.fws.gov"+link.get('href')
				data  = soup1.find_all("script")[19].string
				sId = re.search('var sId = (.+?);', data).group(1)
				for link1 in soup.find_all('a'):
				 if ("county-modal") in str(link1.get('href')):
				  eventId = link1.get('href').split("-")[-1]
				table = soup.find('table', id='pop')
				tdRows = table.findAll('td')
				enlistedDate =tdRows[1].get_text()
				countyURL = 'https://ecos.fws.gov/ecp/pullreports/catalog/species/report/species/export?filter=/species@sid='+str(sId)+'&filter=/species@id='+str(eventId)+'&filter=/species/current_range_county@name%20is%20not%20null&columns=/species@cn;/species/current_range_county@name,state_abbrev&format=csv'
				with requests.Session() as s:
					download = s.get(countyURL)
					decoded_content = download.content.decode('utf-8')
					cr = csv.reader(decoded_content.splitlines(), delimiter=',')
					county_list = list(cr)
					county_str=''
					countyLine = 0
					for county in county_list:
					 if countyLine>0:
					  county_str+=county[1]+'_'+county[2]+'|'
					 countyLine +=1
				petetionTable = soup.find("table", {"id": "petitions-data-table"})
				rows = petetionTable.find_all('tr')
				petetion_str=''
				for pRow in rows:
				 tds = pRow.find_all("td")
				 tdNum = 0
				 pDate=''
				 pAction=''
				 for td in tds:
				  if (tdNum ==1):
				   pDate = td.text
				  elif (tdNum ==4):
				   pAction = td.text
				  tdNum +=1
				 if (len(pDate)>0):
				  petetion_str+=pDate+'_'+pAction+'|'
				fileNameArr = str(file).split("_")
				speciesFinal.write(row[0]+ ",\"" + row[1] + "\"," + fileNameArr[1] + "," + fileNameArr[0] + "," + imgURL + "," + enlistedDate.strip()+ ",\"" + str(county_str.strip())+ "\",\"" + str(petetion_str.strip()) + "\"," + row[4] +"\n")
				browser.close()
				browser.quit()
				imgURL=''
				enlistedDate=''
				county_str=''
				petetion_str=''
			line_count += 1    
print('End Of Code')
	
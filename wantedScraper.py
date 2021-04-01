import requests
import re
import json
from string import capwords
from bs4 import BeautifulSoup as BS

def infoCreator(link):
    '''
    returns a dictionary of the info on the fugitive
    Scrapes data from individual fugitive pages and then sorts it into
    a dictionary within a dictonary
    '''
    
    page = requests.get(link)
    page = page.content
    soup = BS(page, "html.parser")
    
    #outer dictionary
    info = {}
    
    #grabs the first and last name
    nameTXT = soup.find('div', {'class':'field field-name-title-field field-type-text field-label-hidden field-wrapper'}).text
    names = nameTXT.split(',', 1)
    lastName = names[0].upper()
    firstName = names[1].replace(' ', '').upper()
    
    info['firstname'] = firstName
    info['lastname'] = lastName
    
    #pulls the block of the html where the text is contained and grabs all keys and values
    block = soup.find('div', {'class':'wanted_top_right'})
    allKey = block.find_all('h2', {'class':'field-label'})
    allVal = block.find_all('ul', {'class':'links inline'})
    
    #inner dictionary that is keyed about
    about = {}
    
    #loops through and stores all the info in the about dictionary 
    for x in range(len(allKey)):
        key = allKey[x].text
        key = key.replace(": ", "")
        key = key.replace(" ", "_")
        key = key.lower()
        val = allVal[x].text
        val = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', val)
        
        about[key] = val
    
    info['about'] = about
    
    return info



jsonDic = {}

url = "https://eumostwanted.eu/"

mainPage = requests.get(url)
formattedPage = mainPage.content
soupMain = BS(formattedPage, "html.parser")

#finds the source name and source code
sourceCode = soupMain.find('title').text.replace(" |", "")
sourceName = soupMain.find('a', {'id':'ENFASTLink2'}).text

#adds the first 3 elements to the dictionary
jsonDic['source_code'] = sourceCode
jsonDic['source_name'] = sourceName
jsonDic['source_url'] = url

#creates an fills an array of links to the indvidual pages
links = []
for block in soupMain.find_all('div', {'class':'views-field views-field-title'}):
    for link in block.find_all('a'):
        links.append(link.get('href'))

#leaving this comment in because when I initially ran this block it picked up this link
#links.remove('https://eumostwanted.eu/legal-notice')

people = []
for link in links:
    people.append(infoCreator(link))

jsonDic['people'] = people

jsonFile = open("mostWanted.json", "w")
jsonFile.write(json.dumps(jsonDic, indent = 4))
jsonFile.close()
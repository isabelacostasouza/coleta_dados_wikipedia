#Author: Isabela Costa Souza (isabela.costasouza10@gmail.com)
#GitHub: https://github.com/isabelacostasouza/wikipedia_data_collector
#Date: 06.16.2019

import requests
from bs4 import BeautifulSoup

#read file "wikipages.txt" and storage the titles of the articles wanted
list_pages = set()
f=open("wikipages.txt", "r")
if f.mode == 'r':
    contents = f.read()
    contents = contents.splitlines()
    for content in contents:
        list_pages.add(content)

#set the wikipedia's URLs
url = 'https://en.wikipedia.org/wiki/Talk:{}'
final_url = ''

#create a loop that runs all the pages on the list
for page_name in list_pages:
    
    #format the URLs with the page's name
    final_url = url.format(page_name)

    #get the URL's html
    page = requests.get(final_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    #get the tags where the classes are
    body = soup.find(class_="wpbs-inner outercollapse")
    divs = body.find_all(class_="tmbox")

    #Create a .txt file with all the classes of the page
    file_name = str(page_name) + "Page_classes"
    f= open(file_name,"w+")
    
    #save all the classes in the .txt file
    for div in divs:
        div02 = div.find(class_="wpb-header")
        div03 = div02.find("td")
        links = div03.find_all("a")
        class01 = div.find("th")
        for link in links:
            f.write(str(link.contents[0]) + ": " + str(class01.contents[0]) + "\n")
        f.write("\n")
    
    f.close()

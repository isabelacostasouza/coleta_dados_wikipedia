#Author: Isabela Costa Souza (isabela.costasouza10@gmail.com)
#GitHub: https://github.com/isabelacostasouza/wikipedia_data_collector
#Date: 06.14.2019

import requests
from bs4 import BeautifulSoup

#create a list with the title os the pages you wanna get information of. Ex.: Brazil and Tennis
list_pages = {'Brazil', 'Tennis'}

#create a loop that runs all the pages on the list
for page_name in list_pages:

    #set the wikipedia's URLs with the page's name
    final_url = ("https://en.wikipedia.org/w/api.php?action=query&titles=" + page_name + "&prop=links&pllimit=max")

    #get the URL's html
    page = requests.get(final_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    #get HTML's class highlight, that contains the tag 'pre', that contains the class 's2', that contains the links of the page 
    page = soup.find(class_="mw-highlight")
    pre = page.find('pre')
    links = pre.find_all(class_='s2')

    cont = -1

    #get the index where the links start to appear
    for i in range(len(links)-1):
        if(links[i].contents[0] == '"links"'):
            cont = i
            break

    page_links = []

    #get all the links os the page
    for i in range((len(links)-cont)-1):
        if(i % 3 == 0):
            page_links.append(links[i + cont].contents[0])

    #Create a .txt file with all the links of the page
    file_name = str(page_name) + "Page_links"
    f= open(file_name,"w+")

    link_url = "https://en.wikipedia.org/wiki/"
    cont = 0

    for link in page_links:
        if(cont > 0):
            aux_url = ""
            link = link.replace('"', '')
            link = link.split(' ')
            for i in range(len(link)):
                if(i > 0):
                    aux_url = aux_url + "_" + link[i]
                else:
                    aux_url = link[i]
            f.write(link_url + str(aux_url) + "\n")
        cont += 1

    f.close()

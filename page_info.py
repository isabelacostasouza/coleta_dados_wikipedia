#Author: Isabela Costa Souza (isabela.costasouza10@gmail.com)
#GitHub: https://github.com/isabelacostasouza/wikipedia_data_collector
#Date: 06.14.2019

import json
import requests
from bs4 import BeautifulSoup

#create a list with the title os the pages you wanna get information of. Ex.: Brazil and Tennis
list_pages = {'Brazil', 'Tennis'}

#set the wikipedia's URLs
url01 = 'https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvlimit=50&titles={}'
url02 = 'https://en.wikipedia.org/w/index.php?title={}&action=history'
link_url = 'https://en.wikipedia.org/w/index.php?title=Brazil&oldid={}'
final_url01 = ''
final_url02 = ''

#create a loop that runs all the pages on the list
for page_name in list_pages:
    
    #format the URLs with the page's name
    final_url01 = url01.format(page_name)
    final_url02 = url02.format(page_name)

    #get the First URL's html
    page = requests.get(final_url01)
    soup = BeautifulSoup(page.text, 'html.parser')

    #get HTML's tag 'page'
    page = soup.find('page')

    #get page's tag 'revisions'
    revisions = page.find('revisions')
    revisions = revisions.find_all('rev')

    comments = []
    parentIds = []
    revisionIds = []
    timestamps = []
    usernames = []
    links = []
    
    #get data from each revision of the wikipedia page
    for revision in revisions:
        revision = (str(revision)).split('"')
        comments.append(revision[1])
        if(str(revision[3]) == ''):
            parentIds.append(revision[5])
            revisionIds.append(revision[7])
            links.append(link_url.format(revisionIds[len(revisionIds)-1]))
            timestamps.append(revision[9])
            usernames.append(revision[11])
        else:
            parentIds.append(revision[3])
            revisionIds.append(revision[5])
            links.append(link_url.format(revisionIds[len(revisionIds)-1]))
            timestamps.append(revision[7])
            usernames.append(revision[9])
    
    #get the Second URL's html
    page = requests.get(final_url02)
    soup = BeautifulSoup(page.text, 'html.parser')

    #get HTML's class history, that contains the size os the revisions in bytes
    get_sizes = soup.find_all(class_="history-size mw-diff-bytes")
    get_sizes = (str(get_sizes)). split(">")

    sizes = []
    cont = 0
    
    #get size of each revision of the wikipedia page
    for size in get_sizes:
        if(cont % 2 != 0):
            size = (str(size)). split(",")
            final_size = (size[0] + '.' + size[1][0] + size[1][1])
            sizes.append(final_size)
        cont += 1
        
    #Data collected = comments[], parentsIds[], revisionIds[], links, timestamps[], usernames[], sizes[]

    """
    Print data collected: 
    
    print("\n\n------------------ " + page_name + " ------------------\n")
    
    for aux in range(len(revisionIds)):
        print("\nRevision ID: " + revisionIds[aux])
        print("Revision Link: " + links[aux])
        print("Parent ID: " + parentIds[aux])
        print("Timestamp: " + timestamps[aux])
        print("Contributor's username: " + usernames[aux])
        print("Contributor's comment: " + comments[aux])
        print("Revision's size: " + sizes[aux])
    """

    #create a dictionary with the data of each revision
    revision_dic = {}
    for i in range(len(revisionIds)):
      revision_name = "Revision " + revisionIds[i]
      revisionItems_dic = {}
      revisionItems_dic["ID"] = revisionIds[i]
      revisionItems_dic["Parent ID"] = parentIds[i]
      revisionItems_dic["Timestamp"] = timestamps[i]
      revisionItems_dic["Contributor's username"] = usernames[i]
      revisionItems_dic["Contributor's comment"] = comments[i]
      revisionItems_dic["Revision's link"] = links[i]
      revisionItems_dic["Revision's size (bytes)"] = sizes[i]
      revision_dic[revision_name] = revisionItems_dic

    #create a dictionary with all the revisions of the page
    final_dic = {}
    final_dic[str(page_name)] = revision_dic

    #create a JSON file with the disctionary above
    file_name = str(page_name) + "Page_revisions"
    filePathNameWExt = file_name + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(final_dic, fp)

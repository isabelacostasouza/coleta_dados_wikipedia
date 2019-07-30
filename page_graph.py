#Author: Isabela Costa Souza (isabela.costasouza10@gmail.com)
#GitHub: https://github.com/isabelacostasouza/wikipedia_data_collector
#Date: 30.07.2019

import requests
from bs4 import BeautifulSoup

#add new item to a dictionary
def add_or_append(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)
    
#get all the links of a page
def page_links(page_name):
    #set the wikipedia's URLs with the page's name
    final_url = ("https://en.wikipedia.org/w/api.php?action=query&titles=" + input_page + "&prop=links&pllimit=max")

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

    page_links = {}
    cont2 = 0

    #get all the links os the page
    for i in range((len(links)-cont)-1):
        if(i % 3 == 0 and cont2 != 0):
            add_or_append(page_links, page_name, links[i + cont].contents[0])
        cont2 += 1

    return page_links

#writes in a file, a graph page -> links
def write_graph(file, page, page_links):
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
            file.write(page + ", " + str(aux_url) + "\n")
        cont += 1
        
#main function        
def main():
    #requests and stores the input page 
    input_page = input()

    #create lists of visited pages, pages to visit and the final dictionary to store all the graphs
    visited_edges = list()
    visit_edges = [input_page]
    final_dict = dict()

    #create a loop white the 'pages to visit' list is not empty
    while((len(visit_edges)) != 0):
        #create the new edge, it's page links and adds it to the dictionary
        edge = visit_edges[0]
        new_edges = page_links(edge)
        final_dict.update(new_edges)
        
        #remove the new edge from the 'pages to visit' file and adds it to the 'visited pages' file
        visit_edges.remove(visit_edges[0])
        visited_edges.insert(len(visited_edges), edge)

        #adds all the non-repeted links to the 'pages to visit' file
        for i in range(len(new_edges[edge])):
        if((new_edges[edge][i] in visited_edges) or (new_edges[edge][i] in visit_edges)):
          pass
        else:
            visit_edges.insert(len(visit_edges), new_edges[edge][i])
            
        '''
        #print the progress
        print("\nVisited:\n")
        print(visited_edges)
        print("\nVisiting: " + str(len(visit_edges)) + " pages\n")
        '''

    #Create a .txt file with all the links of the page
    file_name = str(input_page) + "Page_graph"
    file = open(file_name, "w+")

    #Adds all the information in the file
    keys = final_dict.keys()
    for key in keys:
      values = final_dict[key]
      write_graph(file, key, values)
    file.close()
    
main()

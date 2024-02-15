import os
import urllib.request as ul
from bs4 import BeautifulSoup as soup
import requests as req
import re
import sys

#Change in the directory where you want the article's link stored
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

#function retrieving the articles on a single PubMed page. The standard PubMed webpage displays 10 articles
def dl_intel(url, pure_url):
    #Initializing variables
    responseTxt_4 = ''
    
    #Opening links to articles used to trim the HTML data
    DOI_trash = open('DOI_trash.txt', 'w')
    
    #Obtain HTML data
    client = req.get(url)
    htmldata = client.text
    client.close()
    
    #this part finds the data we look for thanks to HTML beacons, here we want to find the PMID because an article link is always in the form https://pubmed.ncbi.nlm.nih.gov/<PMID>
    db = soup(htmldata, "html.parser")
    locator = db.findAll('a', {'class':'docsum-title'}, href = True)  
    locator_2 = re.findall(r'(?<=href="/)\w+', str(locator))
    links = [i for i in locator_2]
    
    #reforge the url and store it in a new list
    clean_links = [str(pure_url + str(i.strip()) + '/') for i in links]

    for i in clean_links:        
        #We can now use the reforged URL to access each article in the webpage
        site_2 = ul.Request(i)
        client_2 = ul.urlopen(i)
        htmldata_2 = client_2.read()
        client_2.close()
        
        db_2 = soup(htmldata_2, "html.parser")
        
        #Here we locate each element we need to retrieve and store it. Since some caracters used in the articles are not understood we explicitely encode them in UTF-8.
        locator_date = db_2.findAll('span', {'class':'cit'})
        try :
            date = str(re.findall("\d{4}", str(locator_date))[0])
        except :
            continue
        
        locator_4 = db_2.findAll('a', {'class':'id-link'})
        for n in locator_4:
            responseTxt_4 = n.text.encode('UTF-8')
        responseTxt_4 = str(responseTxt_4.strip())
        responseTxt_4 = responseTxt_4[2:-1]
        
        #Store the DOI of the articles and the date they were written
        DOI_trash.write(responseTxt_4 + '\t' + date + '\n')
    
    DOI_trash.close()
    return True

#This function's sole purpose is to pass to the next page in PubMed. It is possible to set a limit to how many pages you want to collect the articles' link from.
def switch_page(url, pure_url):
    #find the limit number of pages to go through
    client = req.get(url)
    htmldata = client.text
    client.close()
    db = soup(htmldata, "html.parser")
    locator = db.findAll('span', {'class':'value'})  
    limite = int(re.findall('[0-9]+', str(locator[0]))[0])//10

    count = 1
    link = url
    
    #Open our definitive file
    Results = open('Results.txt', 'w')
    
    while count <= limite :
        print(dl_intel(link, pure_url), 'Progression :', (count/limite)*100)
        link = url + '&page=' + str(count)
        count+=1
        K = open('DOI_trash.txt', 'r')
        for lines in K.readlines():
            Results.write(lines)
            
    K.close()
    return 'All Done !'

if __name__ == "__main__":
    url = str(sys.argv[1])
    pure_url = 'https://pubmed.ncbi.nlm.nih.gov/'
    switch_page(url, pure_url)
    

import urllib.request as ul
from bs4 import BeautifulSoup as soup
import requests as req
import re
import os

#Change in the directory where you want the article's link stored
os.chdir('C:\\PATH\\TO\\DIRECTORY\\DESIRED')

#function retrieving the articles on a single PubMed page. The standard PubMed webpage displays 10 articles
def dl_intel(url, pure_url):
    #Initializing variables
    responseTxt_3 = ''
    responseTxt_4 = ''
    
    #Opening files used to trim the HTML data
    def_file = open('Def_file.txt', 'w')
    DOI_trash = open('DOI_trash.txt', 'w')
    
    #Obtain HTML data
    client = req.get(url)
    htmldata = client.text
    client.close()
    
    #this part finds the data we look for thanks to HTML beacons, here we want to find the PMID because an article link is always in the form https://pubmed.ncbi.nlm.nih.gov/<PMID>
    db = soup(htmldata, "html.parser")
    locator = db.findAll('a', {'class':'docsum-title'}, href = True)  
    locator_2 = re.findall(r'(?<=href="/)\w+', str(locator))
    links = open('datafile.txt', 'w')
    
    #store the PMID in a file
    for i in locator_2:
        links.write(str(i) + '\n')
    links.close()
    
    tri = open('datafile.txt')
    clean_doc = open('cleandata.txt', 'w')
    
    #reforge the url and store it in a new txt file
    for i in tri.readlines():
        clean_doc.write(pure_url + str(i.strip()) + '/' + '\n')
    clean_doc.close()
    print('done')
    K = open('cleandata.txt')
    for i in K.readlines():
        
        #We can now use the reforged URL to access each article in the webpage
        site_2 = ul.Request(i)
        client_2 = ul.urlopen(i)
        htmldata_2 = client_2.read()
        client_2.close()
        
        db_2 = soup(htmldata_2, "html.parser")
        
        #Here we locate each element we need to retrieve and store it. Since some caracters used in the articles are not understood we explicitely encode them in UTF-8.
        locator_date = db_2.findAll('span', {'class':'cit'})
        try :
            date = str(re.findall('\d{4}', str(locator_date))[0])
        except :
            continue
        locator_2 = db_2.findAll('div', {'class':'abstract'})
        for k in locator_2:
            responseTxt_2 = k.text.encode('UTF-8')
            
        locator_3 = db_2.findAll('p', {'class': 'sub-title'})
        for f in locator_3:
            responseTxt_3 = f.text.encode('UTF-8')
        
        locator_4 = db_2.findAll('a', {'class':'id-link'})
        for n in locator_4:
            responseTxt_4 = n.text.encode('UTF-8')
        responseTxt_4 = str(responseTxt_4.strip())
        responseTxt_4 = responseTxt_4[2:-1]
        
        #Each element is then stored in different file depending on wheter we need it or not for our analysis
        trash_file = open('trash_file.txt', 'w')        
        trash_file.write(str(responseTxt_2))
        trash_file.write(str(responseTxt_3))
        
        #Store the DOI of the articles and the date they were written
        DOI_trash.write(responseTxt_4 + '\t' + date + '\n')
        trash_file.close()
    
    DOI_trash.close()
    K.close()             
    def_file.close()   
    return 'Finished'

#print(dl_intel('https://pubmed.ncbi.nlm.nih.gov/?term=mitochondria&page=1', ['Mitochondria', 'mitochondria','mitochondrial'], 'https://pubmed.ncbi.nlm.nih.gov/', [1,1,1]))


#This function's sole purpose is to pass to the next page in PubMed. It is possible to set a limit to how many pages you want to collect the articles' link from.
def switch_page(url, pure_url, limite):
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
print(switch_page('https://pubmed.ncbi.nlm.nih.gov/?term=Illumina+sequencing+eukaryote&filter=simsearch2.ffrft&filter=years.2010-2023', 'https://pubmed.ncbi.nlm.nih.gov/', 100))


#1,742,870 articles
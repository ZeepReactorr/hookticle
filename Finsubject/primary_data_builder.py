from bs4 import BeautifulSoup as soup
import numpy as np
import requests as req
import re
import os
import time

#Change into a directory where to store the outputed files containing the primary data for the training dataset
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

#Function to filter all beacons and elements that are not text in HTML data
def filter_web(txt):
    #Initialize output
    output = ''
    
    #Define the elements we want to filter out of the raw HTML data
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'footer',
        'style',
        ]
    
    for t in txt:
        #t.parent.name refers to the type of the t element which is looped through the text. If t's origin is in the blacklist, the it is taken out
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

#Function to retrieve the abstract
def dl_intel(url,type_sample):
    #Open output file to write in it
    def_file = []
    
    #get HTML data
    client = req.get(url)
    htmldata = client.text
    client.close()    
    
    #Locate the desired data : here we want to filter out the reviews 
    db = soup(htmldata, "html.parser")
    locator = db.findAll('div', {'class':'abstract-content selected'})  
    abstracts = re.sub(", (.*?)(?=.</div>|<div)", "2K3Y", str(locator))
    abstracts = re.sub("\n|\t", "", abstracts)
    abstracts = re.sub("<[^\>]+>", "", abstracts)
    abstracts = abstracts[1:]
    abstracts = abstracts[:-2]

    abstracts = abstracts.split("2K3Y")
    return abstracts

start = time.time()
#print(dl_intel("https://pubmed.ncbi.nlm.nih.gov/?term=Oxyrrhis+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200", "Metagenomics"))
end = time.time()
#print(f"runtime : {end-start}s")

#Function going from page to page in PubMed.
#This function's sole purpose is to pass to the next page in PubMed. It is possible to set a limit to how many pages you want to collect the articles' link from.
def switch_page(url,type_sample):
    #find the limit number of pages to go through
    client = req.get(url)
    htmldata = client.text
    client.close()
    db = soup(htmldata, "html.parser")
    locator = db.findAll('span', {'class':'value'})  

    nb_articles = ''.join(re.findall('[0-9]+', str(locator[0])))
    limite = (int(nb_articles)//200)+1
    if limite > 2:
        limite = 2
    print(f"estimated runtime {limite*30}s")
    count = 1
    link = url
    
    #Open our definitive file
    Results = []
    
    while count <= limite :
        link = url + '&page=' + str(count)
        print(f"{np.round((count/limite)*100)}%", link)
        count+=1
        Results+=dl_intel(link, type_sample)
        
    Results = [Results, [type_sample]*len(Results)]
    return Results

#Function call to access the desired article's page in pubmed
#print(switch_page('https://pubmed.ncbi.nlm.nih.gov/?term=Oxyrrhis+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200', 'Metagenomics'))

def training_data(url_domain_1, type_1, url_domain_2, type_2):
    datatype_1 = switch_page(url_domain_1, type_1)
    datatype_2 = switch_page(url_domain_2, type_2)

    all_ab = datatype_1[0] + datatype_2[0]
    all_lab = datatype_1[1] + datatype_2[1]

    training_set = [all_ab, all_lab]
    return training_set

#print(training_data('https://pubmed.ncbi.nlm.nih.gov/?term=Oxyrrhis+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200', 'Metagenomics', 'https://pubmed.ncbi.nlm.nih.gov/?term=BYV+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200', 'Culture'))


#for the dataset building
def dataset_page(url, pure_url):  
    #get HTML data
    client = req.get(url)
    htmldata = client.text
    client.close()    

    #Locate the desired data : here we want to filter out the reviews 
    db = soup(htmldata, "html.parser")
    locator = db.findAll('span', {'class':'docsum-journal-citation full-journal-citation'})  

    # <span class="docsum-journal-citation full-journal-citation">Nat Commun. 2023 Nov 3;14(1):7049. doi: 10.1038/s41467-023-42807-0.</span>
    doi_list = re.findall('doi: (.*?)(?=.<|. )', str(locator))

    locator = 'KODE'.join(str(locator).split('</span>'))
    locator = re.sub(';(.*?)(?=.<|<)', "", locator)
    locator = re.sub(";.*", "", locator)
    date_list = re.findall('\d{4}', locator)
    
    intel = [f"{doi_list[i]}\t{date_list[i]}\n" for i in range(0, len(doi_list))]

    return intel


#print(dataset_page('https://pubmed.ncbi.nlm.nih.gov/?term=oxyrrhis+sequencing&filter=simsearch2.ffrft&filter=years.2010-2024', 'https://pubmed.ncbi.nlm.nih.gov/'))

def switch_page_dataset(url, pure_url):
    #find the limit number of pages to go through
    client = req.get(url)
    htmldata = client.text
    client.close()
    db = soup(htmldata, "html.parser")
    locator = db.findAll('span', {'class':'value'})  

    nb_articles = ''.join(re.findall('[0-9]+', str(locator[0])))
    limite = (int(nb_articles)//200)+1
    if limite > 50:
        limite = 50
    count = 1
    link = url
    
    #Open our definitive file
    Results = []
    
    while count <= limite :
        link = url + '&page=' + str(count)
        K=dataset_page(link, pure_url)
        print(f"{np.round((count/limite)*100)}%", link)
        count+=1
        Results += K    
    return Results

#print(switch_page_dataset('https://pubmed.ncbi.nlm.nih.gov/?term=dolphin+sequencing&filter=simsearch2.ffrft&filter=years.2010-2024&size=200', 'https://pubmed.ncbi.nlm.nih.gov/'))


#Function to retrieve the abstract
def sub(url, pure_url, type_sample):
    #Open output file to write in it
    def_file = []
    
    #get HTML data
    client = req.get(url)
    htmldata = client.text
    client.close()    
    
    #Locate the desired data : here we want to filter out the reviews 
    db = soup(htmldata, "html.parser")
    locator = db.findAll('div', {'class':'docsum-content'})  
        
    is_review = str(locator).split("docsum-content")
    is_review = [i for i in is_review if "Review" not in i]
    
    is_review = ''.join(is_review)
    locator_2 = re.findall(r'(?<=href="/)\w+', is_review)
    
    #List of all url from which using the abstract in the training dataset is relevant
    url_pub = [pure_url + str(i.strip()) + '/' for i in locator_2]
    
    #Loop through the list of articles' link
    for i in url_pub:
        #extract HTML data
        meta_data = req.get(i)
        raw_meta = meta_data.content
        db_meta = soup(raw_meta, "html.parser")
        
        #Locate and extract the abstract, and preprocess it with regex to retain only the text
        locator_2 = db_meta.findAll('div', {'class':'abstract'})
        responseTxt_2 = re.sub("\n|\t", "", str(locator_2))
        responseTxt_2 = re.sub("<[^\>]+>", "", responseTxt_2)
        responseTxt_2 = responseTxt_2[1:]
        responseTxt_2 = responseTxt_2[:-2]
        
        #locate the publication's date
        locator_date = db_meta.findAll('span', {'class':'cit'})
        try :
            date = str(re.findall('\d{4}', str(locator_date))[0])
        except :
            continue
        
        #Write all desired information in the output file, all separated by a key to ease the retrieving of the data later on
        def_file.append(f"{responseTxt_2}R4NDOM_KEY{date}R4NDOM_KEY{type_sample}")
    return def_file
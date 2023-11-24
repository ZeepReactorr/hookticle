from bs4 import BeautifulSoup as soup
import requests as req
import re
import os

#Change into a directory where to store the outputed files containing the primary data for the training dataset
os.chdir('C:\\PATH\\TO\\DESIRED\\DIRECTORY')

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
def dl_intel(url, pure_url):
    #Open output file to write in it
    def_file = open('Asbtract_meta.txt', 'w', encoding='utf-8')
    
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
        def_file.write(responseTxt_2 + 'R4NDOM_KEY' + date + 'R4NDOM_KEY' + 'Metagenomics' + '\n')
    
    def_file.close()
    return 'Finished'

#Function going from page to page in PubMed.
def switch_page(url, keywords, pure_url, coefficient, limite):
    count = 1
    link = url
    Results = open('C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\clustering_abstract\\Meta\\Results.txt', 'w', encoding='utf-8')
    while count <= limite :
        print(dl_intel(link, pure_url), (count/limite)*100)
        link = url + '&page=' + str(count)
        count+=1
        K = open('Asbtract_meta.txt', 'r', encoding='utf-8')
        for lines in K.readlines():
            Results.write(lines)
    K.close()
    return 'All Done !'

#Function call to access the desired article's page in pubmed
print(switch_page('https://pubmed.ncbi.nlm.nih.gov/?term=Metagenomics+sample+sequencing&filter=simsearch2.ffrft&filter=years.2010-2024', ['Nanopore', 'Illumina'], 'https://pubmed.ncbi.nlm.nih.gov/', [1], 702))

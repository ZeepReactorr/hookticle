from bs4 import BeautifulSoup as soup
import requests as req
import os
import re
import numpy as np
from matplotlib import pyplot as plt
import urllib.request as ul
import pandas as pd
import seaborn as sns
import multiprocessing
from multiprocessing import Pool
import streamlit as st

#change into the desired directory to store the results of the sorting
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

def hat(i):
    my_raw_data = ''
    #process the line to obtain a viable DOI
    i = i.strip('\n')
    i = i.split('\t')

    #indicates progression of the program
    #print(f"{np.round((index/limite)*100, 2)}%")
            
    #rebuild the link to the full article
    link = 'https://doi.org/' + i[0]
    date = i[1]

    #retrieve data through the DOI. If an error occurs, we switch to the next article
    try :
        retrieved_data = req.get(link)
        my_raw_data = retrieved_data.content
    except Exception:
        return '0'

    output = ''
    #if the DOI redirect toward a PDF, the text is extracted from it in this code

    db_txt = soup(my_raw_data, "html.parser")
    txt = db_txt.find_all(string = True)
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
        if t.parent.name not in blacklist:
            output += '{}'.format(t)

    if len(output) < 500:
        return '1'
        #count_bad_links+=1            
    
    output = re.sub("\n|\r|\rn", '', output) 
    output = output[output.find('Abstract'):].lower()
    try : 
        output = str(output[:max([m.start() for m in re.finditer('references', output)])])
    except : 
        output = str(output)    
    
    return output, link, date

def sci(keywords):
    #global limite, index, count_bad_links, number
    #initialization of variables
    keywords = ['NULL'] + keywords
    dico_keywords = {i:0 for i in keywords}
    
    #Opens the document outputed from link_retriever.py
    with open('Results.txt', 'r', encoding='utf-8') as F:
        F = F.readlines()
        limite = len(F)
    
    #Opens output file
    Searched_material = []
    index = 0
    article_not_found = 0
    article_not_accessible = 0

    textbar = "Searching keywords..."
    bar_articles = st.progress(0, text=textbar)

    st.write(f"{multiprocessing.cpu_count()} CPU available for analysis")
    
    try :
        with Pool(processes=multiprocessing.cpu_count()) as pool:
            for output in pool.imap(hat, F):
                #indicates progression of the program
                index+=1
                if len(output) > 2 :
                    bar_articles.progress(np.round((index/limite), 2), text=textbar)
                    output, link, date = output
                    #write the link in the output document if the conditions are fullfilled : if it is exactly the desired material.        
                    dico = {keywords[i]:output.count(keywords[i].lower()) for i in range(0, len(keywords))}
                    dico_keywords[max(dico, key=dico.get)] += 1

                    Searched_material.append(link + '\t' + date + '\t' + str(max(dico, key=dico.get)) + '\n')
                    dico = {}
                else:
                    if output == "1" :
                        article_not_accessible +=1
                    elif output == "0":
                        article_not_found += 1

    except Exception:
        return "Multiproccessing failed"
    
    for key, res in dico_keywords.items():
        st.write(key, res)
    st.write(f"articles not found : {article_not_found}", f"articles not accessible : {article_not_accessible}", sep="\n")
    
    with open('Searched_material.txt', 'w', encoding='utf-8') as final_file :
        for line in Searched_material:
            final_file.write(line)

    #Summarize the results in the console to give a preview of the results
    #print(f'full text retrieved : {number}\t impossible links to retrieve : {count_bad_links}')
    return 'Done'

#print(sci(["illumina", "nanopore"]))

def tendency(keywords):
    #open results files
    results = open('Searched_material.txt', 'r', encoding='utf-8')

    #Process the data in list containing only the date in which the articles were written
    list_material_date = [(i.split('\t')[1].strip('\n'),i.split('\t')[2].strip('\n')) for i in results.readlines()]

    #Initialize the dates to position the temporality of the articles
    dates = [date for date in range(min([int(elt[0]) for elt in list_material_date]), max([int(elt[0]) for elt in list_material_date]))]
    
    #Count each date occurence as each article has an associated publication date. Thus number of date = number of articles
    count_dates = {i:[int(j[0]) for j in list_material_date if j[1] == i] for i in keywords}

    data = []
    for i in count_dates:
        res = [count_dates[i].count(j) for j in dates]
        data.extend(list(zip(dates, res, [i]*len(dates))))

    df = pd.DataFrame(data, columns=['time', 'number of publications', 'keyword'])

    # Plotting
    plt.figure(figsize=(11, 5))
    ax = sns.barplot(df, x='time', y='number of publications', hue='keyword', alpha=0.7)

    # Customize plot
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Publications')
    ax.set_title(f'Global distribution of the publications between {min(dates)} and {max(dates)}')
    ax.spines[['top', 'right']].set_visible(False)
    sns.move_legend(ax, bbox_to_anchor=(1, 0.5), loc='center left', frameon=False)

    plt.savefig(f'plot_{"_".join(keywords)}.png')
    results.close()

#tendency(['virus', 'prokaryote', 'eukaryote'])

def dl_intel(url):  
    #get HTML data
    client = req.get(url)
    htmldata = client.text
    client.close()    

    #Locate the desired data : here we want to filter out the reviews 
    db = soup(htmldata, "html.parser")
    locator = db.findAll('span', {'class':'docsum-journal-citation full-journal-citation'})  
    locator_review = db.findAll('div', {'class':'docsum-content'})  
        
    base = str(locator_review).split("docsum-content")
    del base[0]
    locator = str(locator).split('</span>')
    del locator[-1]

    #les index correspondent 
    is_review = [index for index, val in enumerate(base) if "Review" in val]
    is_review += [index for index, val in enumerate(base) if "doi:" not in val]

    for index in sorted(is_review, reverse=True):
        del locator[index]

    locator = ' KODE '.join(locator) + ' '

    doi_list = re.findall('doi: (.*?)(?=.<|. )', str(locator))
    locator = re.sub(';(.*?)(?=.<|<)', "", locator)
    locator = re.sub(";.*|:", " ", locator)
    locator += ' '
    date_list = re.findall(' \d{4} ', locator)

    assert(len(doi_list) == len(date_list))
    
    intel = [f"{doi_list[i]}\t{date_list[i].strip(' ')}\n" for i in range(0, len(doi_list))]

    return intel

#dl_intel(f"https://pubmed.ncbi.nlm.nih.gov/?term=oxyrrhis+marina+sequencing&sort_order=asc&size=200&filter=simsearch2.ffrft")

#This function's sole purpose is to pass to the next page in PubMed. It is possible to set a limit to how many pages you want to collect the articles' link from.
def switch_page(url):
    #find the limit number of pages to go through
    txt = 0
    client = req.get(url)
    htmldata = client.text
    client.close()
    db = soup(htmldata, "html.parser")
    locator = db.findAll('span', {'class':'value'})  

    nb_articles = ''.join(re.findall('[0-9]+', str(locator[0])))
    limite = (int(nb_articles)//200)+1
    if limite > 30:
        limite = 25
        nb_articles = 25*200
    count = 1
    link = url
    
    #Open our definitive file
    Results = open('Results.txt', 'w')
    
    textbar = "Retrieving articles..."
    bar_retrieval = st.progress(0, text=textbar)

    while count <= limite :
        link = url + '&page=' + str(count)
        K=dl_intel(link)
        bar_retrieval.progress(np.round((count/limite), 2), text=textbar)
        count+=1
        for lines in K:
            Results.write(lines)

    st.write(f'{nb_articles} articles retrieved !\n')
    return ''

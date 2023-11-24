import requests as req
import PyPDF2
from io import BytesIO
import os

#change into the desired directory to store the results of the sorting
os.chdir('C:\\PATH\\TO\\DESIRED\\DIRECTORY')

def sci(url, keywords, pure_url, coefficient, sci_url, ru_url, limite):
    Searched_material = 0
    signal = 1
    #Opens the document outputed from link_retriever.py
    F = open('Results.txt', 'r')
    #Opens output file
    Searched_material = open('Searched_material.txt', 'w')
    count_bad_links = 0
    line = ''
    number = 0
    count = 0
    
    #loop through each lines of the file with a link in each
    for i in F.readlines():
        doc = open('document.txt', 'w+')  
        
        #process the line to obtain a viable DOI
        i = i.strip('\n')
        i = i.split('\t')
        
        #indicates progression of the program
        print(signal, (signal/1000)*100)
        signal+=1
        link = 'https://doi.org/' + i[0]
        date = i[1]
        
        #retrieve data through the DOI. If an error occurs, we switch to the next article
        try :
            retrieved_data = req.get('https://doi.org/' + i[0])
            my_raw_data = retrieved_data.content
        except:
            count_bad_links +=1
            print('1 bad links =', count_bad_links)
            continue
        
        #if the DOI redirect toward a PDF, the text is extracted from it in this code
        if b'%PDF' in my_raw_data:
            data = BytesIO(my_raw_data)
            try :
                read_pdf = PyPDF2.PdfReader(data)
                for page in range(len(read_pdf.pages)):
                    txt = read_pdf.pages[page].extract_text()
                    txt = txt.encode('UTF-8', errors = 'ignore')
                    txt = txt.strip()
                    doc.write(str(txt))
                doc.close()
                
            except:
                pass
                    
        else:
            print('else')
            doc.write(str(my_raw_data))
            doc.close()
                
        M = open('document.txt', 'r')
        
        #write the link in the output document if the conditions are fullfilled : if it is exactly the desired material.        
        for line in M.readlines():
            line = line.lower()
            if keywords[0].lower() in line:
                Searched_material +=1
                Searched_material.write(link + '\t' + date + '\n')

        print('illu =', Searched_material)
    
    #Summarize the results in the console to give a preview of the results
    print('not PDF', count) 
    print('Corresponding articles found :', number)
    print('impossible links to retrieve :', count_bad_links)
    
    print('Searched_material :', Searched_material)

    return 'Done'
    
print(sci('https://pubmed.ncbi.nlm.nih.gov/?term=eukaryote+sequencing&filter=years.2014-2023&sort=date', ['Searched_material', 'Nanopore', 'PacBio'], 'https://pubmed.ncbi.nlm.nih.gov/', [1], 'https://sci-hub.ru/', 'https://moscow.sci-hub.ru/', 1000))
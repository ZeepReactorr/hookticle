import requests as req
import PyPDF2
from io import BytesIO
import os

#change into the desired directory to store the results of the sorting
os.chdir('C:\\PATH\\TO\\DESIRED\\DIRECTORY')

def sci(keywords, limite):
    #initialization of variables
    signal = 1
    keywords = ['NULL'] + keywords
    dico_keywords = {i:0 for i in keywords}
    
    #Opens the document outputed from link_retriever.py
    F = open('DOI_trash.txt', 'r', encoding='utf-8')
    
    #Opens output file
    Searched_material = open('Searched_material.txt', 'w', encoding='utf-8')
    count_bad_links = 0
    number = 0
    
    #loop through each lines of the file with a link in each
    for i in F.readlines():        
        #process the line to obtain a viable DOI
        i = i.strip('\n')
        i = i.split('\t')
        
        #indicates progression of the program
        print(signal, (signal/limite)*100)
        signal+=1
        
        #rebuild the link to the full article
        link = 'https://doi.org/' + i[0]
        date = i[1]
        
        #retrieve data through the DOI. If an error occurs, we switch to the next article
        try :
            retrieved_data = req.get(link)
            my_raw_data = retrieved_data.content
        except:
            count_bad_links +=1
            continue
        
        output = ''
        #if the DOI redirect toward a PDF, the text is extracted from it in this code
        if b'%PDF' in my_raw_data:
            data = BytesIO(my_raw_data)
            try :
                read_pdf = PyPDF2.PdfReader(data)
                for page in range(len(read_pdf.pages)):
                    txt = read_pdf.pages[page].extract_text()
                    txt = txt.encode('UTF-8', errors = 'ignore')
                    output = str(txt.strip())                
            except:
                pass
        
        #filter the CSS and html beacons out of the file             
        else:
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
                    
            output = re.sub("\n|\r|\rn", '', output) 
            output = output[output.find('Abstract'):]
            output = str(output[:output.find('References')])            
                        
        #write the link in the output document if the conditions are fullfilled : if it is exactly the desired material.        
        dico = {keywords[i]:output.count(keywords[i]) for i in range(0, len(keywords))}
        dico_keywords[max(dico, key=dico.get)] += 1
        Searched_material.write(link + '\t' + date + '\t' + str(max(dico, key=dico.get)) + '\n')
        dico = {}
                
    for i in dico_keywords:
        print(i, str(dico_keywords[i]))

    #Summarize the results in the console to give a preview of the results
    print('Corresponding articles found :', number)
    print('impossible links to retrieve :', count_bad_links)

    return True
    
print(sci(['material_1', 'material_2', 'material_3'], 1000))

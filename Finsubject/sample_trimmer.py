import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from dataclasses import dataclass
import random
import requests as req
from bs4 import BeautifulSoup as soup
import re

#change here the end of files name depending on the compared data
S = 'NE'

#change into the directory where the primary data is stored
os.chdir('C:\\PATH\\TO\\OUTPUT\\DIRECTORY')
main_dir = os.getcwd()

#Opens the directory where the training abstract set is stored
abstracts_data = open("C:\\PATH\\TO\\DIRECTORY\\ABSTRACT\\TRAINING\\DATASET", 'r', encoding='utf-8')

#Creation of the class abstract to ease the data manipulation
@dataclass()
class abstract():
    text : str
    date : str
    sample : str

data= []
for i in abstracts_data.readlines():
    try :
        #Initialize variables to the respective data
        a, d, s = i.split('R4NDOM_KEY')
    except:
        continue
    #append the variable to their designed data
    data.append(abstract(text = a, date = d, sample = s.strip('\n')))

#shuffle the data to randomize the order and avoid a manichean partition of the dataset in two categories
random.shuffle(data)
#creates a list of all the abstract's text
list_abstract = [i.text for i in data]
#creates a parallel list with the type of sample
list_label = [i.sample for i in data]

#function definition for text prediction
def predict_sample_type(article_text):
    text_vector = vectorizer.transform([article_text])
    prediction = classifier.predict(text_vector)
    return prediction[0]

#Articles' text retrieval, preprocessing before they are tried and classified
def sample_repartitor(file_in, ARTICLE_TYPE_1, ARTICLE_TYPE_2):
    #initialize variables
    count_bad_links = 0
    F = open(file_in, 'r')
    ARTICLE_TYPE_1 = open(ARTICLE_TYPE_1, 'w')
    article_type_1 = 0
    ARTICLE_TYPE_2 = open(ARTICLE_TYPE_2, 'w')
    cult = 0
    
    #Loop through the articles and process the lines to obtain articles in one variable and the publication date in another
    for url in F.readlines():
        doc = open('document.txt', 'w', encoding = 'UTF-8')   
        url = url.strip('\n')
        url = url.split('\t')
        date = url[1]
        url = url[0]
        
        #get the HTML data
        try :
            retrieved_data = req.get(url)
            my_raw_data = retrieved_data.content
            my_raw_text = retrieved_data.text
        except:
            count_bad_links +=1
            print('1 bad links =', count_bad_links)
            continue
        
        #Process the entire HTML data and retrieve only the text
        db_txt = soup(my_raw_text, "html.parser")
        txt = db_txt.find_all(string = True)
        output = ''
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
                output += '{} '.format(t)
        
        #Use regex to polish the text, and take out the references from the text as it could alter the classification. Everything before the abstract is also filtered out.
        output = re.sub("\n|\r|\rn", '', output) 
        output = output[output.find('Abstract'):]
        output = output[:output.find('References')]
        doc.write(str(output))
        doc.close()   
                
        #write the results of the classification in a txt file
        M = open('document.txt', 'r', encoding = 'UTF-8')
        for line in M.readlines():
            line = line.lower()
            sample_type = predict_sample_type(line)
            if sample_type == 'ARTICLE_TYPE_1' :
                article_type_1 +=1
                ARTICLE_TYPE_1.write(url + '\t' + date + '\n')
            if sample_type == "ARTICLE_TYPE_2":
                cult +=1
                ARTICLE_TYPE_2.write(url + '\t' + date + '\n')
                
        M.close()
    
    return 'ALl done !'

#Iterate the model multiple times, which each time a retraining of the Model (it forgets everything each time so there is no overfitting)
all_score = []
for i in range(0, 30):
    random.shuffle(data)
    list_abstract = [i.text for i in data]
    list_label = [i.sample for i in data]
    
    abstract_train, abstract_test, y_train, y_test = train_test_split(list_abstract, list_label, test_size=0.3, random_state=1000)
    vectorizer = CountVectorizer()

    vectorizer.fit(abstract_train)
    X_train = vectorizer.transform(abstract_train)
    X_test = vectorizer.transform(abstract_test)

    scaler = preprocessing.StandardScaler(with_mean=False).fit(X_train)

    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    all_score.append(score)
    print("Accuracy:", score)

    sample_repartitor(f'C:\\PATH\\TO\\ARTICLE\\FILE\\LINK\\TO\\ANALYZE\\LINKS_TO_ANALYZE.txt',
                      f'C:\\PATH\\TO\\RESULTS\\RESULTS_{S}\\article_type_1{S}' + str(i) +'.txt',
                      f'C:\\PATH\\TO\\RESULTS\\RESULTS_{S}\\article_type_2{S}' + str(i) +'.txt')
    print(i/10)

#creates a file dedicated to gather the accuracy of the model for eahc iteration    
accuracy = open('C:\\PATH\\TO\\RESULTS\\RESULTS_{S}\\accuracy_{S}.txt', 'w')    
for i in all_score:
    accuracy.write("Accuracy:" + str(i) + '\n')
accuracy.close()

print('done')
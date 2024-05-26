import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from dataclasses import dataclass
import random
import requests as req
from bs4 import BeautifulSoup as soup
import re
import time
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, RocCurveDisplay, roc_auc_score
from matplotlib import pyplot as plt

#Change into a directory where to store the outputed files containing the primary data for the training dataset
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

import primary_data_builder as pdb

#Creation of the class abstract to ease the data manipulation
@dataclass()
class article():
    text : str
    date : str
    sample : str

def abstract_retriever(url_domain_1, type_1, url_domain_2, type_2):
    abstract_list = pdb.training_data(url_domain_1, type_1, url_domain_2, type_2)
    dico = dict(zip(['Abstract', 'Type'], abstract_list))
    df = pd.DataFrame(data=dico)  
    return df

"""
print(abstract_retriever('https://pubmed.ncbi.nlm.nih.gov/?term=oxyrrhis+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200',
                         'Metagenomics',
                         'https://pubmed.ncbi.nlm.nih.gov/?term=BYV+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200', 
                         'Culture Samples'))
"""

#function definition for text prediction
def predict_sample_type(article_text):
    text_vector = vectorizer.transform([article_text])
    prediction = classifier.predict(text_vector)
    return prediction[0]

#Articles' text retrieval, preprocessing before they are tried and classified
def sample_repartitor(url_to_test, pure_url, articles_types):
    #initialize variables
    n = 1
    count_bad_links = 0
    results = []
    articles_to_test = pdb.switch_page_dataset(url_to_test, pure_url)
    counter_dico = {i:0 for i in articles_types}

    #Loop through the articles and process the lines to obtain articles in one variable and the publication date in another
    for url in articles_to_test:
        url = url.strip('\n')
        url = url.split('\t')
        date = url[1]
        url = f"https://doi.org/{url[0]}"
        #get the HTML data
        try :
            retrieved_data = req.get(url)
            my_raw_data = retrieved_data.content
            my_raw_text = retrieved_data.text
        except Exception:
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

        if len(output)< 1000:
            count_bad_links+=1
            continue
        sample_type = predict_sample_type(output)
        counter_dico[sample_type] +=1

        results.append(article(text=output, date=date, sample=sample_type))

        print(f"{round(n/len(articles_to_test)*100, 2)}%")
    print(counter_dico)
    return results

start_training_set = time.time()
"""
data = abstract_retriever('https://pubmed.ncbi.nlm.nih.gov/?term=oxyrrhis+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200',
                         'Metagenomics',
                         'https://pubmed.ncbi.nlm.nih.gov/?term=BYV+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200', 
                         'Culture Samples')

"""
data = abstract_retriever('https://pubmed.ncbi.nlm.nih.gov/?term=Metagenomics+sample+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200',
                           'Metagenomics',
                           'https://pubmed.ncbi.nlm.nih.gov/?term=Culture+sample+sequencing+NOT+Review&filter=simsearch2.ffrft&filter=years.2010-2024&format=abstract&size=200',
                             'Culture Samples')


print(data.shape)   

end_training_set = time.time()
print(f"training set for 2x2000 abstract took {(end_training_set-start_training_set)/60} minutes to build")

start_classfying = time.time()
#Iterate the model multiple times, which each timex a retraining of the Model (it forgets everything each time so there is no overfitting)
for i in range(1):
    st = time.time()

    list_abstract = [abstract for abstract in data["Abstract"]]

    list_label = data["Type"].values

    abstract_train, abstract_test, y_train, y_test = train_test_split(list_abstract, list_label, test_size=0.3, random_state=1000)
    vectorizer = CountVectorizer()
    vectorizer.fit_transform(abstract_train)

    X_train = vectorizer.transform(abstract_train)
    X_test = vectorizer.transform(abstract_test)

    scaler = preprocessing.StandardScaler(with_mean=False).fit(X_train)
    classifier = LogisticRegression(max_iter=500000)

    classifier.fit(X_train, y_train)
    score = (classifier.score(X_train, y_train), classifier.score(X_test, y_test))
    y_pred = classifier.predict(X_test)
    print(accuracy_score(y_pred, y_test))
    
    conf_mat = confusion_matrix(y_test, y_pred, labels=classifier.classes_)
    print(conf_mat)
    #CMD = ConfusionMatrixDisplay(conf_mat, display_labels=['Metagenomic', "Culture samples"])
    #CMD.plot()
    #plt.show()
    
    #label 0 == Culture Samples
    #label 1 == Metagenomics
    
    pred_ori = classifier.predict_proba(X_test)
    
    y_pred_proba = classifier.predict_proba(X_test)[:,1]
    y_pred_proba_0 = classifier.predict_proba(X_test)[:,0]

    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba, pos_label=1)
    
    print(fpr, tpr)
    
    fpr_0, tpr_0, thresholds_0 = roc_curve(y_test, y_pred_proba, pos_label=0)

    score_auc = roc_auc_score(y_test, y_pred_proba)
    score_auc_0 = roc_auc_score(y_test, y_pred_proba_0)
    
    plt.plot([0, 1],[0, 1], '--')
    plt.plot(fpr, tpr)
    
    plt.plot(fpr_0, tpr_0)    
    print('score auc', score_auc, score_auc_0)
    
    print("Accuracy:", score)
    
    sample_repartitor('https://pubmed.ncbi.nlm.nih.gov/?term=dinoflagellates%20sequencing&filter=simsearch2.ffrft&filter=years.2010-2024&size=200',
                       'https://pubmed.ncbi.nlm.nih.gov/',
                         ["Metagenomics", "Culture Samples"])
    print('Ok')

end_classifying = time.time()
print(f"One iteration of classifying of 642 articles took {(end_classifying-start_classfying)/60}")
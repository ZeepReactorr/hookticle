from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import os 
import numpy as np

result_dir = 'C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\dino\\test_wos\\'
#corrected_meta = open('C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\clustering_abstract\\Trial_2_categories\\results_IP\\corrected_meta.txt', 'w')
#corrected_cult = open('C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\clustering_abstract\\Trial_2_categories\\results_IP\\corrected_cult.txt', 'w')

os.chdir(result_dir)

ban_cult_txt = open('C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\dino_nophoto\\cult_uneasy.txt', 'r')
ban_meta_txt = open('C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\dino_nophoto\\meta_uneasy.txt', 'r')

ban_cult = [i.strip('\n') for i in ban_cult_txt.readlines()]

ban_meta = [i.strip('\n') for i in ban_meta_txt.readlines()]


all_doi_cult = []
all_doi_meta = []
iter_meta = 0
iter_cult = 0
for i in os.listdir():
    if 'Cult' in i:
        cult = open(i, 'r')
        all_doi_cult += [i for i in cult.readlines() if i.split('\t')[0] not in ban_cult]
        iter_cult +=1
    if 'Meta' in i:
        meta = open(i, 'r')
        all_doi_meta += [i for i in meta.readlines() if i.split('\t')[0] not in ban_meta]
        iter_meta +=1
        

transfer_cult = [i for i in all_doi_cult]
transfer_meta = [i for i in all_doi_meta]
set_doi_meta = set(transfer_meta)
set_doi_cult = set(transfer_cult)

dico_set_cult = {i:all_doi_cult.count(i) for i in set_doi_cult}
dico_set_meta = {i:all_doi_meta.count(i) for i in set_doi_meta}
#results_cult = [dico_set_cult[i] for i in set_doi_cult if dico_set_cult[i] >= np.round(iter_cult*1/3) and dico_set_cult[i] <=np.round(iter_cult*2/3)]
results_cult = [dico_set_cult[i] for i in set_doi_cult]
#results_meta = [dico_set_meta[i] for i in set_doi_meta if dico_set_meta[i] >= np.round(iter_meta*1/3) and dico_set_meta[i] <=np.round(iter_meta*2/3)]
results_meta = [dico_set_meta[i] for i in set_doi_meta]
print('Precision score : \n', 'Metagenomics :' ,1-len(results_meta)/len(dico_set_meta), 'Culture samples :', 1-len(results_cult)/len(dico_set_cult))

dates_cult = [i for i in range(1, iter_cult+1)]
dates_meta = [i for i in range(1, iter_meta+1)]


plt.bar([i+0.3 for i in dates_cult], [results_cult.count(i) for i in dates_cult], color = 'b', label='Culture samples', width = 0.6)
plt.bar(dates_meta, [results_meta.count(i) for i in dates_meta], color = 'r', label='Metagenomics samples', width = 0.6)
plt.xlabel('Number of iterations')
plt.ylabel('Number of articles')
plt.title('Number of articles in each iteration \n for dinoflagellates sequencing \n without Suessiales')
plt.legend(bbox_to_anchor=(1.05, 1), loc = 'upper left')
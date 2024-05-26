from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import os 
import numpy as np

result_dir = 'C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\dino\\test_wos\\'
os.chdir(result_dir)

dates = [i for i in range(2010, 2024)]
iteration = [i for i in range(0, 7)]

dico_meta = {str(i):[] for i in range(2010, 2024)}
dico_cult = {str(i):[] for i in range(2010, 2024)}

ban_cult_txt = open('C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\dino_nophoto\\cult_uneasy.txt', 'r')
ban_meta_txt = open('C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\dino_nophoto\\meta_uneasy.txt', 'r')

ban_cult = [i.strip('\n') for i in ban_cult_txt.readlines()]
ban_cult = []
ban_meta = [i.strip('\n') for i in ban_meta_txt.readlines()]
ban_meta = []
for i in os.listdir():
    if 'Cult' in i:
        cult = open(i, 'r')
        dates_cult = [i.split('\t')[1].strip('\n') for i in cult.readlines() if i.split('\t')[0] not in ban_cult]
        count_cult = [dico_cult[str(i)].append(dates_cult.count(str(i))) for i in range(2010, 2024)]
    if 'Meta' in i:
        meta = open(i, 'r')
        dates_meta = [i.split('\t')[1].strip('\n') for i in meta.readlines() if i.split('\t')[0] not in ban_meta]
        count_meta = [dico_meta[str(i)].append(dates_meta.count(str(i))) for i in range(2010, 2024)]
    #if 'accu' in i:
        #accuracy = open(i, 'r')
        #all_acc = [float(i.split(': ')[1].strip('\n')) for i in accuracy.readlines()]
        #dico_accu = {iteration[i]:all_acc[i] for i in range(0, len(all_acc))}

        
fig = figure(figsize=(11,5))
ax = fig.add_subplot(111)
plt.plot(dico_cult.keys(), dico_cult.values(), '.', color = 'b')
plt.plot(dico_cult.keys(), [np.average(i) for i in dico_cult.values()], color = 'b', label = ' Culture samples'+ '\n' +' average')

plt.plot(dico_meta.keys(), dico_meta.values(), '.', color = 'r')
plt.plot(dico_meta.keys(), [np.average(i) for i in dico_meta.values()], color = 'r', label = " Metagenomic samples"+"\n" +" average")
plt.legend(bbox_to_anchor=(1.05, 1), loc = 'upper left')

plt.xlabel('Time')
plt.ylabel('Number of research articles')
plt.grid()

#ax2 = ax.twinx()
#ax3 = ax.twiny()
#ax2.set_ylim(0,1)
#ax2.plot(iteration, [i for i in dico_accu.values()], color='y', label = 'Model accuracy')
#ax2.legend(bbox_to_anchor=(1.05, 0.80), loc= 'upper left')
plt.title('Comparative usage of Metagenomic and Culture samples' + '\n' +'in dinoflagellates sequencing')
plt.show()


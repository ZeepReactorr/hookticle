from matplotlib import pyplot as plt
import os 
import numpy as np

#change into the directory where the results are stored
result_dir = 'C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\dino\\test_wos\\'
os.chdir(result_dir)

ban_cult_txt = open('C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\dino_nophoto\\cult_uneasy.txt', 'r')
ban_meta_txt = open('C:\\Subpbiotech_cours\\BT4\\Stage_MNHN\\SOA_nanopore\\approfondissement\\Sample_type_analysis\\Test_topic_clustering\\dino_nophoto\\meta_uneasy.txt', 'r')

ban_cult = [i.strip('\n') for i in ban_cult_txt.readlines()]

ban_meta = [i.strip('\n') for i in ban_meta_txt.readlines()]

#initialize variables
lines_cult = []
lines_meta = []
iterations = 0

#fill lists through processing of data
for i in os.listdir():
    if 'Cult' in i:
        cult = open(i, 'r')
        lines_cult.append(len([i for i in cult.readlines() if i.split('\t')[0] not in ban_cult]))
        cult.close()
    if 'Meta' in i:
        meta = open(i, 'r')
        lines_meta.append(len([i for i in meta.readlines() if i.split('\t')[0] not in ban_meta]))
        iterations+=1
        meta.close()

print('Average number of article_type_1 :', np.average(lines_cult), ' with standard deviation :', np.std(lines_cult), '\n'
     'Average number of article_type_2 :', np.average(lines_meta), ' with standard deviation :', np.std(lines_meta))

plt.plot([i for i in range(0, iterations)], lines_cult, 'b')
plt.plot([i for i in range(0, iterations)], lines_meta, 'r')
plt.ylim(0,350)
plt.xlabel('Number of iterations')
plt.ylabel('Number of articles')
        
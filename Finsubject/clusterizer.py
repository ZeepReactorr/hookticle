from matplotlib import pyplot as plt
import os 

#change into the directory where the results are stored
result_dir = 'C:\\PATH\\TO\\RESULTS\\DIRECTORY'
os.chdir(result_dir)

#Variable initialization
all_doi_cult = []
all_doi_meta = []
iter_meta = 0
iter_cult = 0
#Looping through results' files to get data from them all and build a list with the content of all the files
for i in os.listdir():
    if 'cult' in i:
        cult = open(i, 'r')
        all_doi_cult +=cult.readlines()
        iter_cult +=1
    if 'meta' in i:
        meta = open(i, 'r')
        all_doi_meta += meta.readlines()
        iter_meta +=1
        
#set an non-inherited list to keep the full one and place the new one in a set
transfer_cult = [i for i in all_doi_cult]
transfer_meta = [i for i in all_doi_meta]
set_doi_meta = set(transfer_meta)
set_doi_cult = set(transfer_cult)

#fill a dictionnary to count the number of occurence of each link in the full list
dico_set_cult = {i:all_doi_cult.count(i) for i in set_doi_cult}
dico_set_meta = {i:all_doi_meta.count(i) for i in set_doi_meta}

#compute the results per iterations
#Uncomment to display only error rate articles or the full repartition over iterations


#results_cult = [dico_set_cult[i] for i in set_doi_cult if dico_set_cult[i] >= np.round(iter_cult*1/3) and dico_set_cult[i] <=np.round(iter_cult*2/3)]
results_cult = [dico_set_cult[i] for i in set_doi_cult]
#results_meta = [dico_set_meta[i] for i in set_doi_meta if dico_set_meta[i] >= np.round(iter_meta*1/3) and dico_set_meta[i] <=np.round(iter_meta*2/3)]
results_meta = [dico_set_meta[i] for i in set_doi_meta]
print('Precision score : \n', 'Article type 1 :' ,1-len(results_meta)/len(dico_set_meta), 'Article type 2 :', 1-len(results_cult)/len(dico_set_cult))

#initialize dates
dates_cult = [i for i in range(1, iter_cult+1)]
dates_meta = [i for i in range(1, iter_meta+1)]

#plot the results slightly shifted to the right for one of them in order to see both barplots
plt.bar([i+0.2 for i in dates_cult], [results_cult.count(i) for i in dates_cult], color = 'b', label='Culture samples', width = 0.6)
plt.bar(dates_meta, [results_meta.count(i) for i in dates_meta], color = 'r', label='Metagenomics samples', width = 0.6)
plt.xlabel('Number of iterations')
plt.ylabel('Number of articles')
plt.title('Number of articles in each iteration \n for Nanopore eukaryotes samples')
plt.legend(bbox_to_anchor=(1.05, 1), loc = 'upper left')

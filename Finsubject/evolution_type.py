from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import os 
import numpy as np

#change into the directory where the results are stored
result_dir = 'C:\\PAHT\\TO\\RESULTS\\DIRECTORY'
os.chdir(result_dir)

#initialize dates range
dates = [i for i in range(2010, 2024)]
iteration = [i for i in range(0, 7)]

#initialize dictionnaries
dico_article_type_1 = {str(i):[] for i in range(2010, 2024)}
dico_article_type_2 = {str(i):[] for i in range(2010, 2024)}


#fill dictionnaries through processing of data
for i in os.listdir():
    if 'article_type_2' in i:
        article_type_2 = open(i, 'r')
        dates_article_type_2 = [i.split('\t')[1].strip('\n')  for i in article_type_2.readlines()]
        count_article_type_2 = [dico_article_type_2[str(i)].append(dates_article_type_2.count(str(i))) for i in range(2010, 2024)]
    if 'article_type_1' in i:
        article_type_1 = open(i, 'r')
        dates_article_type_1 = [i.split('\t')[1].strip('\n') for i in article_type_1.readlines()]
        count_article_type_1 = [dico_article_type_1[str(i)].append(dates_article_type_1.count(str(i))) for i in range(2010, 2024)]

#plot the results
fig = figure(figsize=(11,5))
ax = fig.add_subplot(111)
plt.plot(dico_article_type_2.keys(), dico_article_type_2.values(), '.', color = 'b')
plt.plot(dico_article_type_2.keys(), [np.average(i) for i in dico_article_type_2.values()], color = 'b', label = ' Culture samples'+ '\n' +' average')

plt.plot(dico_article_type_1.keys(), dico_article_type_1.values(), '.', color = 'r')
plt.plot(dico_article_type_1.keys(), [np.average(i) for i in dico_article_type_1.values()], color = 'r', label = " Metagenomic samples"+"\n" +" average")
plt.legend(bbox_to_anchor=(1.05, 1), loc = 'upper left')

plt.xlabel('Time')
plt.ylabel('Number of research articles')
plt.grid()

plt.title('Comparative of article_type_1 with article_type_2' + '\n' +'in <domain>')


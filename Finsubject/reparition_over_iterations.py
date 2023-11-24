from matplotlib import pyplot as plt
import os 
import numpy as np

#change into the directory where the results are stored
result_dir = 'C:\\PATH\\TO\\RESULTS\\DIRECTORY'
os.chdir(result_dir)

#initialize variables
lines_cult = []
lines_meta = []
iterations = 0

#fill lists through processing of data
for i in os.listdir():
    if 'cult' in i:
        cult = open(i, 'r')
        lines_cult.append(len(cult.readlines()))
        cult.close()
    if 'meta' in i:
        meta = open(i, 'r')
        lines_meta.append(len(meta.readlines()))
        iterations+=1
        meta.close()

print('Average number of article_type_1 :', np.average(lines_cult), ' with standard deviation :', np.std(lines_cult), '\n'
     'Average number of article_type_2 :', np.average(lines_meta), ' with standard deviation :', np.std(lines_meta))

plt.plot([i for i in range(0, iterations)], lines_cult, 'b')
plt.plot([i for i in range(0, iterations)], lines_meta, 'r')
plt.xlabel('Number of iterations')
plt.ylabel('Number of articles')
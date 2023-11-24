from matplotlib import pyplot as plt
import os

#Change in the directory where the results are stored
os.chdir('C:\\PATH\\TO\\RESULTS\\DIRECTORY')
main_dir = os.getcwd()

#Initialize the dates to position the temporality of the articles
dates = [i for i in range(2010, 2024)]

#open results files
res_euka = open('illumina_all.txt')
res_proka = open('nanopore_all.txt')

#Process the data in list containing only the date in which the articles were written
dates_euka = [i.split('\t')[1].strip('\n') for i in res_euka.readlines()]
dates_proka = [i.split('\t')[1].strip('\n') for i in res_proka.readlines()]

#Count each date occurence as each article has an associated publication date. Thus number of date = number of articles
count_date_euka = [dates_euka.count(str(i)) for i in range(2010, 2024)]
count_date_proka = [dates_proka.count(str(i)) for i in range(2010, 2024)]

#display the results on a barplot
plt.bar(dates, count_date_euka, color = 'b', label = 'Illumina sequencing')
plt.bar(dates, count_date_proka, color = 'r', label = 'NSTs ')
plt.xlabel('time')
plt.ylabel('number of publications')
plt.title('Global distribution of the publications using Illumina or NSTs'+  '\n'+ 'in their methods between 2010 and 2023')
plt.ylim(0,900)

plt.legend()

res_euka.close()
res_proka.close()

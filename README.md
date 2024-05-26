# Exatool

Exatool is written in python and is able to retrieve the full text of an article (when free). Its purpose is to allow a better understanding of the material used by the scientific community using a keyword research. Python scripts to visualize the data are also available.
The development is still ongoing and currently limited to the PubMed database of research articles. 

**If you have questions, find bugs, or have ideas of features you would like to propose, do not hesitate to reach out at mattgitqna@gmail.com**

If you know for sure your query will not be too long, a friendlier GUI is available here : https://exatools.streamlit.app/
**This web-app is limited in terms of runtime : if you are searching more than 1000 articles I advise to use the terminal version. I am currently working on setting up a more efficient web-app.**

If you wish to avoid the limitations of the web-app, but still need a GUI a rudimentary app can be downloaded here : https://github.com/ZeepReactorr/exatools/releases/download/release_1.0/exatool_WINDOWS_1.0_setup.exe <br>

Be aware that it **will be slower** than if you used a terminal :).

## Prerequisite 

To run the programs smoothly, you need to have installed the following packages : 
- bs4
- requests
- numpy
- matplotlib

All those packages can be installed with `pip install <package_name>` from the terminal

## Installation

To install the Exatool program, run the following command line in your terminal :
```sh
git clone https://github.com/ZeepReactorr/exatools
```

## Usage

To run the program, enter the following command line in your terminal, filling the gaps with the required parameters :
```sh
python ~/PATH/TO/exatool.py ~/PATH/TO/OUTPUT_DIR 'Pubmed URL' keyword_1 keyword_2... keyword_n
```

The program will keep the progression updated in the console. The ouptut graphical plot will be saved in the output directory you indicated as well as the intermediary files. 
**Be careful that the date range in your Pubmed query and indicated date range variable __match__, if they don't, the plot will not be correct.** <br>
**Make sure that the URL is between quotes, as the command will return an error otherwise.**

Example of prompt : 

```sh
python C:/PATH/TO/exatool.py C:/PATH/TO/OUTPUT/DIRECTORY 'https://pubmed.ncbi.nlm.nih.gov/?term=prokaryote+sequencing&filter=simsearch2.ffrft' Illumina Nanopore
```

This will count the respective occurency of Nanopore or Illumina sequencing for articles related to Prokaryote sequencing throughout pubmed and automatically generate a graph displaying just that. 

> The **reviews** are **filtered out**. Only research papers with methods are taken into account.

## Results

Sample results for a query about the most used sequencing techniques for dinoflagellates between 2011 and 2023:
![plot_nanopore_sanger_pacbio_illumina](https://github.com/ZeepReactorr/hookticle/assets/151944715/dc86374f-0822-4d35-9331-c7baa9d6d8a9)

Sample results for the most used mapping tool in ONT bioinformatics between 2002 and 2023: 
![plot_minimap_kraken](https://github.com/ZeepReactorr/hookticle/assets/151944715/9574660c-c830-48c2-9667-589b15deac2d)


# Finsubject

Finsubject aims to provide a comprehensive view of a field of research based on the researcher's own standards. It relies on Logistic Regression and Natural Language Processing algorithms to do so. Currently the program has only been tested and verified on classifying research articles about sequencing depending on whether they were working on Metagenomic samples or Culture samples. The model has been generalized, and work is currently focused on generalizing it in order to make it efficient no matter the subject. Afterward the model will be made fully available and user friendly.

### Installation

Coming soon.

### Usage

Finsubject action is divided in 4 steps
- Field definition 
- Model training
- Testing set definition
- Classification of the Testing set

### Metrics

In addition to the usual metric scores of Machine Learning (accuracy score, F1, Confusion matrix), Finsubject will provide a detailed report on the query with the following graph.

Results plot : <br>
![image](https://github.com/ZeepReactorr/hookticle/assets/151944715/6c60fc99-b0d5-4961-b0f3-49e7953fb346) <br>

Number of article classified in each category at every iteration of the model : <br>
![image](https://github.com/ZeepReactorr/hookticle/assets/151944715/92c2098f-0c7d-4f0b-842e-3904b550c105) <br>

Numbre of articles in each category at each model iteration : <br>
![image](https://github.com/ZeepReactorr/hookticle/assets/151944715/124c9137-beb6-4834-938d-5f494222a380) <br>

# Credit

If you found anny of these tool useful during your research, please cite the corresponding model :

BETTIATI M. (2024). Exatool [Python]. https://github.com/ZeepReactorr/hookticle (Original work published 2024)

BETTIATI M. (2024). Finsubject [Python]. https://github.com/ZeepReactorr/hookticle (Original work published 2024)







## Exatool

Exatool is written in python and is able to retrieve the full text of an article (when free). Its purpose is to allow a better understanding of the material used by the scientific community using a keyword research. Python scripts to visualize the data are also available.
The development is still ongoing and currently limited to the PubMed database of research articles. 

## Finsubject

Finsubject aims to provide a comprehensive view of a field of research based on the researcher's own standards. It relies on Logistic Regression to do so. Currently the program has only been tested and verified on classifying research articles about sequencing depending on whether they were working on Metagenomic samples or Culture samples. The development to generalize the model is ongoing and currently limited to the Pubmed database of research articles. Also written in Python, scripts are available to verify the results of the script.

## pipeline_2

The first draft of a pipeline for _de novo_ transcriptome assembly. Currently the Read to Read Overlap Finding step fails, and I am working on a fix. The pipeline is written in bash. Also working on finding a cool name.

## **Abstract : A study on how to adapt nanopore sequencingto strictly heterotrophic dinoflagellates.**

Dinoflagellates are a diverse, ubiquitous order of unicellular eukaryotes and have been
studied since the XIX century. About 2 500 species have been reported and multiple trophic
modes have been described (i.e. photo-autotrophy and/or phago-heterotrophy). Most of the
studies focus on photosynthetic dinoflagellates because they are easier to maintain in culture.
Moreover, there is a generalized lack of information on dinoflagellates omics because obtaining
their genomes presents technical challenges (e.g., size ranging from 3 to 250 Gb and high proportion of repeated elements), resulting in an underrepresentation of this phylum in the past
years while high-throughput sequencing technologies entered the laboratories. This study aims
to develop molecular biology protocols for 3rd generation sequencing (i.e. nanopore techniques) on unicellular eukaryotes, and enhance the ability to study culture challenging heterotrophic dinoflagellates through a flexible workflow meant for a small number of cells (<500
cells). The overall goal being to produce a reference transcriptome from Oxyrrhis marina, a
phago-heterotrophic dinoflagellate species. <br>
<br>
During this internship I first developed web scraping scripts in order to establish a quantitative state of the art and tendencies of the studies led for the last ten years. Secondly, I developed a primary workflow for cell isolation, nucleic acid extraction and processing before sequencing on MinION mk1C from Oxford Nanopore Technologies. Thirdly I set up a bioinformatic pipeline to treat the sequences obtained by third generation nanopore sequencing. <br>
<br>
The results of the bibliometric data scraped from Pubmed and Web of Science acknowledged the relevance of the research project. 30% of the studies on dinoflagellates in the last
three years targeted less than 1% of the phylum consisting only of autotrophic species. The
nucleic acid extraction protocol yielded poor results, with a 2% yield for DNA and unknown
for RNA. Due to a material defection RNA quality and concentration could not be determined.
In addition, part of the bioinformatic pipeline I developed and benchmarked on a test sample
was defective and yielding incorrect results. However the clustering branch of the pipeline
worked properly and was able to produce usable data. <br>
<br>
This four month internship shed light on the challenges to tackle to pursue this project.
Following through the project with a different approach for the nucleic acid extraction could
lead to better results. A corrective should be applied to the bioinformatic pipeline in order for
the sequencing data to be processed properly. Anyhow, continuing further the project will be
beneficial as shown by the bibliometric analysis. On a personal note, I volunteered to extend
the internship during the next semester to pursue this endeavour. <br>

Keywords : Dinoflagellates, Nanopore sequencing, molecular biology,
bioinformatics, Transcriptomic.




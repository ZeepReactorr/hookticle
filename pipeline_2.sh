#!/bin/bash

#Calling the basecaller guppy : 

#Set up the model file for Guppy to treat hereafter based on the sequencing kit that was used
/PATH/TO/guppy_basecaller --print_workflows 

#Start the actual basecalling step on the binary sequencing files, indicating the flow cell types used
/PATH/TO/ont-guppy-cpu/bin/guppy_basecaller -i /PATH/TO/fast5 -s /PATH/TO/guppy_out -c dna_r9.4.1_450bps_hac.cfg --num_callers 2 --cpu_threads_per_caller 1

echo "starting trimming"

#call to the pychopper trimmer specialized for cDNA trimming. Input : fastq file from the basecaller. output : fastq trimmed file
cdna_classifier.py /PATH/TO/untrimmed.fastq ~/PATH/TO/trimmed_sequences.fastq

echo "Trimming done"

echo "Read to read mapping with flye"

#call to the assembler flye to find read to read overlaps. Input : trimmed reads as fastq file. Output : fasta file of assembled reads.
python ~/Flye/bin/flye --nano-corr ~/PATH/TO/trimmed_sequences.fastq --out-dir ~/PATH/TO/OUTPUT_DIRECTORY/ --threads 4

#error correction step to adjust precision of the assembly
racon ~/PATH/TO/trimmed_sequences.fastq ~/PATH/TO/alignment.paf ~/PATH/TO/OUTPUT_DIRECTORY/assembly.fasta > ~/PATH/TO/OUTPUT_DIRECTORY/flye_corrected.racon.consensus.fasta

echo "starting clustering with cd-hit"

#Clustering module. Input : fastq file from trimming step. Output : fasta file from clustered reads.
cd-hit-est -i ~/PATH/TO/trimmed_sequences.fastq -o ~/PATH/TO/OUTPUT_DIRECTORY/output.fasta -c 0.9 -n 8 -M 16000 -T 4

echo "alignement try out"

#Alignment of clustered reads on the assembly. Input : clustered reads from cd-hit and assembly from flye. Output : alignment file to viewable in IGV.
minimap2 -a -x map-ont ~/PATH/TO/clustered_sequences.fasta ~/PATH/TO/assembly.fasta | samtools view -S -b > ~/PATH/TO/OUTPUT_DIRECTORY/mapped_unsorted.bam


#!/bin/bash

echo "Guppy is too long to be done here : using pre-made results"

echo "starting trimming"

cdna_classifier.py ~/course_data/dataset/Dmel.4.filt.fastq ~/course_data/pipeline_cdna/pychopper_trimming/output.fastq

echo "Trimming done"

echo "Read to read mapping with flye"

python ~/Flye/bin/flye --nano-corr ~/course_data/Trimming/pychoppered.fastq --out-dir ~/course_data/assembly/flye/ --threads 4

echo "starting clustering with cd-hit"

cd-hit-est -i ~/course_data/cd-hit_test/pychopper/output.fasta -o ~/course_data/cd-hit_test/cd-hit_results/output1.fasta -c 0.9 -n 8 -M 16000 -T 4

echo "alignement try out"

minimap2 -a -x map-ont ~/course_data/Trimming/pychoppered.fastq ~/course_data/assembly/shasta/Assembly.fasta | samtools view -S -b > ~/course_data/alignment/trimmed_reads/mapped_unsorted.bam

racon ~/course_data/Trimming/pychoppered.fastq ~/course_data/assembly/flye/minimap_flye.racon.paf ~/course_data/assembly/flye/assembly.fasta > ~/course_data/error_correction/flye_corrected.racon.consensus.fasta

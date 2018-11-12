# IndelSearcher_CRISPR_CAS9

### Prerequisite ###
    OS Requirements: Linux(Ubuntu 16.04)
    Install time: about 30 minutes
    
    - python2.7
    pip install numpy==1.12.1 pandas==0.20.1
    or
    - anaconda python2.7
    conda install numpy=1.12.1 pandas=0.20.1
    
    EMBOSS:6.6.0.0, needle
    http://emboss.sourceforge.net/download/
    

### Usage ###

    ./Project_list.txt
    Write the one project name per line
    
    /Input/FASTQ/<project_name>/<sample_name>.fastq
    /Input/Reference/<project_name>/barcode.txt
    /Input/Reference/<project_name>/Reference_sequence.txt
    /Input/Reference/<project_name>/Target_region.txt
    
    Test
    python2.7 Run_indel_searcher_ver3.0.py --pam_type Cas9 --pam_pos Forward
    
    Detailed options
    python2.7 Run_indel_searcher_ver3.0.py -h
    
    Output
    /Output/<project_name>/Summary_result/Final_indel_result_<project_name>.tsv
    Barcode            Total_indel  Total IND/TOT  Match    Info
    CACCGACACACACACAGCAC    20      105     0.19    20.0    66M1I:12:60.0, 67M2D:8:40.0
    
    /Output/<project_name>/Summary_result/Summary_result.tsv
    Barcode                Total  Insertion Deletion Complex Total_indel IND/TOT
    CACCGACACACACACAGCAC    105      12        8        0        20      0.190476190476
    
# Random sequence generator

### Prerequisite ### 
    - python2.7
    pip install numpy==1.13
    or
    - anaconda python2.7
    conda install numpy=1.13
    
### Usage ###
    python2.7 Random_sequence_generator.py 1000 23 0.2 0.3 0.2 0.3 random_seq.txt

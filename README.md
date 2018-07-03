# IndelSearcher_CRISPR_CAS9

### Prerequisite ###
    python2.7
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
    
    
# Random sequence generator

### Prerequisite ###
    python2.7
    
### Usage ###
    python2.7 Random_sequence_generator.py 1000 23 0.2 0.2 0.2 0.3 random_seq.txt

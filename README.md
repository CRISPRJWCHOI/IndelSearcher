# IndelSearcher_CRISPR_CAS9

### Prerequisite ###
    conda install numpy=1.12.1 pandas=0.20.1
    
    EMBOSS:6.6.0.0, needle
    http://emboss.sourceforge.net/download/

### Usage ###

    ./Project_list.txt
    Write the project names per line
    
    /Input/FASTQ/<project_name>/sample1.fastq
    /Input/Reference/<project_name>/barcode.txt
    /Input/Reference/<project_name>/Reference_sequence.txt
    /Input/Reference/<project_name>/Target_region.txt
    
    python2.7 Run_indel_searcher_ver3.0.py Cas9 --pam_type Cas9 --pam_pos Forward

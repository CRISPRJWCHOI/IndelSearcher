#!/usr/bin/env python

import os, sys
import pandas as pd
import subprocess as sp
from pdb import set_trace

sOutput_dir = sys.argv[1]

def Parsing_summary():

    if not os.path.isdir("{outdir}/Summary_result".format(outdir=sOutput_dir)):
        os.mkdir("{outdir}/Summary_result".format(outdir=sOutput_dir))
    sp.call('cat {outdir}/Summary/*.txt > {outdir}/Summary/Summary_all.txt'.format(outdir=sOutput_dir), shell=True)
    dfSummary         = pd.read_table('{outdir}/Summary/Summary_all.txt'.format(outdir=sOutput_dir), header=None)
    dfSummary.columns = ['Barcode', 'Total', 'Insertion', 'Deletion', 'Complex']
    dfSummary = dfSummary.groupby(['Barcode']).sum()
    dfSummary['Total_indel'] = dfSummary['Insertion'] + dfSummary['Deletion'] + dfSummary['Complex']
    dfSummary['IND/TOT']     = dfSummary['Total_indel'] / dfSummary['Total']
    dfSummary['IND/TOT'].fillna(0, inplace=True)
    dfSummary.to_csv('{outdir}/Summary_result/Summary_result.tsv'.format(outdir=sOutput_dir), sep='\t')


def Annotate_final_result():
	
    dfCount_INDEL = pd.read_table('{outdir}/result/freq/freq_result/Indel_summary.txt'.format(outdir=sOutput_dir), header=None)
    dfSummary     = pd.read_table('{outdir}/Summary_result/Summary_result.tsv'.format(outdir=sOutput_dir), index_col='Barcode')

    dfCount_INDEL[0] = dfCount_INDEL[0].str.replace('.INDEL_freq.txt', '')
    dfCount_INDEL.set_index(0, inplace=True)
    dfConcat_result = pd.concat([dfCount_INDEL, dfSummary.loc[:,['Total_indel', 'Total', 'IND/TOT']]],axis=1)
    dfConcat_result.dropna(inplace=True)
    dfConcat_result = dfConcat_result.reset_index()
    dfConcat_result = dfConcat_result.loc[:,['index','Total_indel', 'Total', 'IND/TOT', 1,2]]
    dfConcat_result.columns = ['Barcode', 'Total_indel', 'Total', 'IND/TOT', 'Match','Info']
    dfConcat_result = dfConcat_result.round(2)
    dfConcat_result.to_csv('{outdir}/Summary_result/Final_indel_result.tsv'.format(outdir=sOutput_dir), sep='\t', index=False)

if __name__ == '__main__':
    Parsing_summary()
    Annotate_final_result()

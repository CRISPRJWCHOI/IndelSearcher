#!/usr/bin/python2.7

import os, sys
import multiprocessing as mp
import subprocess as sp
from datetime import datetime
import pdb
from optparse import OptionParser


class Path_info(object):

    def __init__(self, sProject,  options):

        self.sProject       = sProject
        self.iCore          = options.multicore
        self.iChunk_size    = options.chunk_number
        self.sQual_cutoff   = options.base_quality
        self.sGap_open      = options.gap_open                   # needle aligner option
        self.sGap_extend    = options.gap_extend                 #
        self.sEnd_open      = options.end_open                   #
        self.sEnd_extend    = options.end_extend                 #
        self.iInsertion_win = options.insertion_window      # Insertion window 0,1,2,3,4
        self.iDeletion_win  = options.deletion_window       # Deletion window 0,1,2,3,4
        self.sPAM_type      = options.pam_type                   # CRISPR type : Cpf1(2 cleavages), Cas9(1 cleavage)
        self.sPAM_pos       = options.pam_pos                    # Barcode target position : Forward (barcode + target), Reverse (target + barcode)


        self.sBarcode = './Input/Reference/%s/Barcode.txt' % self.sProject
        self.sReference_seq = './Input/Reference/%s/Reference_sequence.txt' % self.sProject
        self.sTarget_seq = './Input/Reference/%s/Target_region.txt' % self.sProject
        self.sRef_path = './Input/Reference/%s/Reference.fa' % self.sProject  # reference e.g.Consensus.fa

        for sFile in os.listdir('./Input/FASTQ/%s' % (self.sProject)):
            self.sFastq_name = '.'.join(sFile.split('.')[:-1])
            print(self.sFastq_name)
        self.sInput_file = './Input/FASTQ/%s/%s.fastq' % (self.sProject, self.sFastq_name)
        self.sInput_list = './Input/FASTQ/%s/%s.txt' % (self.sProject, self.sFastq_name)  # splited input file names for fastq processing

        self.sOutput_dir = './Output/%s' % self.sProject
        if os.path.isdir(self.sOutput_dir):
            print("Result file already exists. Please remove the output file and try again.\ncd Output\nmv Project_name tmp")
            sys.exit()
        if not os.path.isdir(self.sOutput_dir): os.mkdir(self.sOutput_dir)
        if not os.path.isdir(self.sOutput_dir+'/Summary'): os.mkdir(self.sOutput_dir+'/Summary')                                        
        if not os.path.isdir(self.sOutput_dir+'/result'): os.mkdir(self.sOutput_dir+'/result')
        if not os.path.isdir(self.sOutput_dir+'/result/freq'): os.mkdir(self.sOutput_dir+'/result/freq')
        if not os.path.isdir(self.sOutput_dir+'/result/freq/freq_result'): os.mkdir(self.sOutput_dir+'/result/freq/freq_result')

        self.sInput_path = os.path.dirname(self.sInput_file)
        self.sPair       = 'False'  # FASTQ pair: True, False
        self.sDir        = '/'.join(self.sInput_list.split('/')[:-1])


class Single_node_controller(Path_info):

    def __init__(self, iCore, sProject, options):
        super(Single_node_controller, self).__init__(sProject, options)

    def Split_file(self):

        iTotal_lines = len(open(self.sInput_file).readlines())
        iSplit_num   = iTotal_lines/self.iChunk_size
        if iSplit_num == 0: iSplit_num = 1

        print(iTotal_lines, self.iChunk_size, iSplit_num)

        with open(self.sInput_file) as fq, \
            open(self.sInput_list, 'w') as Out_list:

            for num in range(1, iSplit_num + 1):
                sSplit_file = '%s/%s_%s.fq' % (self.sInput_path, os.path.basename(self.sInput_file), num)
                #if not os.path.isfile(sSplit_file):
                with open(sSplit_file, 'w') as out:
                    Out_list.write(os.path.basename(sSplit_file) + '\n')
                    iCount = 0
                    for sRow in fq:
                        iCount += 1
                        out.write(sRow)
                        if iCount == self.iChunk_size:
                            break

    def Make_reference(self):

        with open(self.sBarcode) as Barcode, \
                open(self.sTarget_seq) as Target, \
                open(self.sReference_seq) as Ref, \
                open(self.sRef_path, 'w') as Output:

            lName = [sBar.replace('\n', '') + ':' + sTar for sBar, sTar in zip(Barcode, Target)]

            for i, sRow in enumerate(Ref):
                Output.write('>' + lName[i] + sRow)

    def Make_indel_searcher_CMD(self):

        lCmd = []
        sReverse = 'None'

        with open(self.sInput_list) as Input:

            for sFile in Input:
                lFile = sFile.replace('\n', '').split(' ')
                sForward = self.sDir + '/' + lFile[0]
                if self.sPair == 'True':
                    sReverse = self.sDir + '/' + lFile[1]

                lCmd.append('./Indel_searcher_ver3.0.py {forw} {reve} {ref} {pair} {GapO} {GapE} {EndO} {EndE} {Insertion_win} {Deletion_win} {PAM_type} {PAM_pos} {Qual} {outdir}'.format(forw=sForward, reve=sReverse,
                            ref=self.sRef_path, pair=self.sPair, GapO=self.sGap_open, GapE=self.sGap_extend, EndO=self.sEnd_open, EndE=self.sEnd_extend, Insertion_win=self.iInsertion_win, Deletion_win=self.iDeletion_win,
                            PAM_type=self.sPAM_type, PAM_pos=self.sPAM_pos, Qual=self.sQual_cutoff, outdir=self.sOutput_dir))
        return lCmd

    def Run_indel_freq_calculator(self):
        sp.call('./Indel_frequency_calculator.py {outdir}'.format(outdir=self.sOutput_dir), shell=True)
        sp.call('./Summary_all_trim.py {outdir}'.format(outdir=self.sOutput_dir), shell=True)


def Run_indel_searcher(sCmd):
    sp.call(sCmd, shell=True)

def Run_multicore(lCmd, iCore):
    print 'lCmd', lCmd
    p = mp.Pool(iCore)
    p.map_async(Run_indel_searcher, lCmd).get()
    p.close()

def Main():
	
    print 'program start: %s' % datetime.now()
   	
    parser = OptionParser("Indel search program for CRISPR CAS9\n<All default option> python2.7 Run_indel_searcher_ver3.0.py --pam_type Cas9 --pam_pos Forward")

    parser.add_option("-t", "--thread", default="1", type="int", dest="multicore", help="multiprocessing number")
    parser.add_option("-c", "--chunk_number", default="400000", type="int", dest="chunk_number", help="split FASTQ, must be multiples of 4. file size < 1G recommendation:40000, size > 1G recommendation:400000")
    parser.add_option("-q", "--base_quality", default="20", dest="base_quality", help="NGS read base quality")
    parser.add_option("--gap_open", default="20", dest="gap_open", help="gap open: 1~100")
    parser.add_option("--gap_extend", default="1", dest="gap_extend", help="gap extend: 0.0005~10.0")
    parser.add_option("--end_open", default="20", dest="end_open", help="end open: 1~100")
    parser.add_option("--end_extend", default="1", dest="end_extend", help="end extend: 0.0005~10.0")
    parser.add_option("-i", "--insertion_window", default="4", type="int", dest="insertion_window", help="a window size for insertions")
    parser.add_option("-d", "--deletion_window", default="4", type="int", dest="deletion_window", help="a window size for deletions")
    parser.add_option("--pam_type", dest="pam_type", help="PAM type: Cas9 Cpf1")
    parser.add_option("--pam_pos", dest="pam_pos", help="PAM position: Forward Reverse")

    options, args = parser.parse_args()

    with open('Project_list.txt') as Project_list:
        for sRow in Project_list:
            sProject   = sRow.replace('\n', '').replace('\r','').replace(' ','')
            Ins_single = Single_node_controller(options.multicore, sProject, options)
            Ins_single.Split_file()
            Ins_single.Make_reference()

            lCmd = Ins_single.Make_indel_searcher_CMD()
            #print(lCmd)
            Run_multicore(lCmd, options.multicore)
            Ins_single.Run_indel_freq_calculator()

    print 'program end: %s' % datetime.now()


if __name__ == '__main__':
    Main()


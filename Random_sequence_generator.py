#!/usr/bin/env python

import sys
import pdb
import numpy as np

number=int(sys.argv[1])
length=int(sys.argv[2])
probA=float(sys.argv[3])
probT=float(sys.argv[4])
probC=float(sys.argv[5])
probG=float(sys.argv[6])
out=sys.argv[7]
# m rows
# n columns

def sequence(m,n):
    out2 = np.empty(shape=(0,0))
    nucleotide = list('ATCG')

    while m > np.shape(out2)[0]:
        out1 = np.random.choice(nucleotide, m*n, p=[probA,probT,probC,probG])
        out1 = out1.reshape(m,n)
        out2 = np.unique(out1, axis=0)

    return out2


np.random.seed(1)

def Main():

    with open(out, 'w') as Output:
        for lCol in sequence(number, length):
            #print(list(lCol))
            #pdb.set_trace()
            Output.write(''.join(lCol.tolist()) +'\n')

    #np.savetxt(out, sequence(number,length), delimiter='\t')

Main()


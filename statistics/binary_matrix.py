#! ../environment/bin/python3.3

#Ranks the disjoint sub-matrices of the entire sequence. Essentially
#checks for linear dependence among fixed length substrings of the
#original sequence.

from bitdata import bitmatrix, partition_bits
from scipy.stats import chi2
from sympy.core.cache import clear_cache
from numpy import sign, sum, array
import ipdb

def bin_mat_list(bitstring, binrows, bincolumns):
    binblocks = partition_bits(bitstring, binrows*bincolumns) 
    bitmatrices = []
    for block in binblocks:
        bitmatrices += [bitmatrix(block, binrows, bincolumns)]
    return bitmatrices

class RankTable:
    full = 0
    semi = 0
    less = 0
    def bin_rank_count(self, matrices):
        for mat in matrices:
            rows = len(mat)
            rank = mrank(mat)
            if rank == rows:
                self.full += 1
            elif rank == rows - 1:
                self.semi += 1
            else:
                self.less += 1

def bin_mat_rank(bitstring, binrows=32, bincolumns=32):
    bitmats = bin_mat_list(bitstring, binrows, bincolumns)
    ranks = RankTable()
    ranks.bin_rank_count(bitmats)
    blockcount = len(bitmats)
    fulleq = (ranks.full - 0.2888*blockcount)**2 / (0.2888*blockcount)
    semieq = (ranks.semi - 0.5776*blockcount)**2 / (0.5776*blockcount)
    lesseq = (ranks.less - 0.1336*blockcount)**2 / (0.1336*blockcount)
    clear_cache()
    return 1 - chi2.cdf(fulleq + semieq + lesseq, 2)

def mrank(matrix): 
    # matrix rank as defined in the NIST specification
    m=len(matrix)
    leni=len(matrix[0])
    def proc(mat):
        for i in range(m):
            if mat[i][i]==0:
                for j in range(i+1,m):
                    if mat[j][i]==1:
                        mat[j],mat[i]=mat[i],mat[j]
                        break
            if mat[i][i]==1:
                for j in range(i+1,m):
                    if mat[j][i]==1: 
                        mat[j]=[int(mat[i][x])^int(mat[j][x]) for x in range(leni)]
        return mat
    maa=proc(matrix)[::-1]
    mu=[i[::-1] for i in maa]
    muu=proc(mu)
    ra=sum(sign([xx.sum() for xx in array(mu)]))
    return ra

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

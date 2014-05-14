#! ../environment/bin/python3.3

#This module provides the frequency monobit test and test within a 
#block. Charmaine Kelly/NIST recommends testing a minimum of 100 bits
#with block sizes (M) such that:
#   M>19
#   M>0.1*bitlength if bitlength < 100

from math import erfc
from numpy import sqrt, floor
from sys import stdin
from scipy.stats import chi2
from bitdata import BitBlock, partition_bits

def mono_frequency(bitblock):
    rootsum = bitblock.count_differences() / sqrt(len(bitblock))
    return erfc(rootsum / sqrt(2))

def block_frequency(bitblock, blocksize=20):
    bitblocks = partition_bits(bitblock, blocksize)
    chi = 0
    blocksize = 0
    for block in bitblocks:
        blocksize = len(block)
        chi_child = (block.bit_ratio(1) - 0.5)**2
        chi += 4*blocksize * chi_child
    return 1 - chi2.cdf(chi, len(bitblocks)-1)

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

def main(bitstring='', blocksize=10):
    if bitstring == '':
        bitstring = stdin.read()
    binary = partition_bits(bitstring, blocksize)
    print('Frequency (Monobit):', mono_frequency(BitBlock(bitstring)))
    print('Frequency within a block:',block_frequency(binary))

if __name__ == '__main__':
    main()

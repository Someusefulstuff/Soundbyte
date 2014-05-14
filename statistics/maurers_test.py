#! ../environment/bin/python3.3

#This test determines how compressible a given sequence is without 
#loss of information. The idea is that a random sequence will be 
#less compressible than a non-random one.

from bitdata import partition_bits
from numpy import log2, sqrt
from math import erfc

def logsum(blocks, initlength):
    initlength = int(initlength)
    pos = {}
    for i in range(1, initlength + 1):
        key = ''.join([str(x) for x in blocks[i - 1]])
        pos[key] = i
    result = 0
    for i in range(initlength + 1,len(blocks) + 1):
        key = ''.join([str(x) for x in blocks[i - 1]])
        try:
            result += log2(i - pos[key])
        except(KeyError):
            result += log2(i)
        finally:
            pos[key] = i
    return result

def theor_param(blocksize):
    """Returns a tuple containing (ExpectedValue, Variance) for 
    a given blocksize. Pre-computed and listed in the NIST manual"""
    if blocksize == 2:
        return (1.5374383, sqrt(1.338))
    if blocksize == 6:
        return (5.2177052, 2.954)
    elif blocksize == 7:
        return (6.1962507, 3.125)
    elif blocksize == 8:
        return (7.1836656, 3.238)
    elif blocksize == 9:
        return (8.1764248, 3.311)
    elif blocksize == 10:
        return (9.1723243, 3.356)
    elif blocksize == 11:
        return (10.170032, 3.384)
    elif blocksize == 12:
        return (11.168765, 3.401)
    elif blocksize == 13:
        return (12.168070, 3.410)
    elif blocksize == 14:
        return (13.167693, 3.416)
    elif blocksize == 15:
        return (14.167488, 3.419)
    elif blocksize == 16:
        return (15.167379, 3.421)
    else:
        print('Blocksize is outside the scope of this test')

def maurers_test(bits, blocksize=6, initlength=640):
    blocks = partition_bits(bits, blocksize)
    ls = 1/(len(blocks) - initlength) * logsum(blocks, initlength)
    ev, var = theor_param(blocksize)
    return erfc(abs(ls - ev) / (sqrt(2) * var))

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

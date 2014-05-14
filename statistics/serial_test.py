#! ../environment/bin/python3.3

#This test is designed to determine whether the number of occurrences of m-bit 
#templates (periodic and aperiodic) that appear in a sequences of bits
#is what you would expect if the sequence is random.

from scipy.stats import chi2
from numpy import sum
from bitdata import partition_bits, BitBlock
from statistics.template_matching import find_matches

def fqs(bits, size):
    tab = []
    form = '0' + str(size) + 'b'
    bits = bits + bits[:size - 1]
    for i in range(2**size):
        patt = BitBlock(format(i, form))
        tab.append(find_matches(bits, patt, False))
    return tab

def serial_test(bits, size=5):
    n = len(bits)
    omeg = [0,0,0]
    for i in range(min(3, size)):
        omeg[i] = 2**(size - i) / n * sum([x**2 for x in fqs(bits, size - i)]) - n
    domeg = [0,0]
    domeg[0] = omeg[0] - omeg[1]
    domeg[1] = omeg[0] - 2*omeg[1] + omeg[2]
    return [1 - chi2.cdf(domeg[0], 2**(size-1)), 1 - chi2.cdf(domeg[1], 2**(size - 2))]

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

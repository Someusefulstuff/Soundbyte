#! ../environment/bin/python3.3

#As with the Serial test, the purpose of this is to look at the frequency of 
#overlapping m-bit patterns across the entire sequence. This test compares 
#the frequency of the overlapping blocks of two consecutive lengths against 
#the expected result of a random sequence.

from statistics.serial_test import fqs
from numpy import log, sum
from scipy.stats import chi2

def entropy_test(bits, size=5):
    n = len(bits)
    tab1 = [1/n * x for x in fqs(bits, size)] 
    tab2 = [1/n * x for x in fqs(bits, size + 1)] 
    omeg = [0,0]
    omeg[0] = sum([x * log(x) for x in tab1 if x >0])
    omeg[1] = sum([x * log(x) for x in tab2 if x >0])
    chisq = 2 * n * (log(2) - omeg[0] + omeg[1])
    return 1 - chi2.cdf(chisq, 2**size)

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

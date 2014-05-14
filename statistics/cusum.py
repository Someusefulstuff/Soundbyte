#! ../environment/bin/python3.3

#This test looks at the maximum excursion from 0 of the random walk
#defined by the cumulative sum of adjusted -1, +1 digits in the sequence.
#The cumulative sum may be considered as a random walk and for a random
#sequence this should be near 0.

from scipy.stats import norm
from numpy import sqrt, floor, max, sum
from math import erf
import ipdb

def max_psum(bits, mode):
    """Computes the maximum partial sum of the sequence. If the mode
    is 0 the direction is forward and if it is 1 it is reversed."""
    bits = bits.transform_bit(0,-1)
    if mode ==1:
        bits.reverse()
    return max([abs(sum(bits[:i + 1])) for i in range(len(bits))])

def cusum(bits, mode=0):
    n = len(bits)
    z = max_psum(bits, mode)
    pvalue = 1
    if z == 0:
        return -1
    start = int(floor((-n / z + 1) * 0.25)) + 1
    stop = int(floor((n / z - 1) * 0.25)) + 2
    sum1 = 0
    for k in range(start, stop):
        sum1 += norm.cdf(((4 * k + 1) * z) / sqrt(n)) 
        sum1 -= norm.cdf(((4 * k - 1) * z) / sqrt(n))
    start = int(floor((-n / z - 3) * 0.25)) + 1
    sum2 = 0
    for k in range(start, stop):
        sum2 += norm.cdf(((4 * k + 3) * z) / sqrt(n)) 
        sum2 -= norm.cdf(((4 * k + 1) * z) / sqrt(n))
    return 1 - sum1 + sum2
    
def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True
    

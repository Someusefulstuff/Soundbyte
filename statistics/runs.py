#! ../environment/bin/python3.3

#This test looks at the total number of uninterrupted runs in a 
#sequence, and looks for evidence of randomness. In particular it 
#focuses on the rate of oscillation between runs of zeroes and ones.

from math import erfc, sqrt
from bitdata import BitBlock, partition_bits, swap_bit

def tau_test(bitblock):
    ones_ratio = bitblock.uniform(1) / len(bitblock)
    if abs(ones_ratio - (0.5)) >= 2/sqrt(len(bitblock)):
            return True
    else:
        return False

def run_count(bitblock):
    runacc = 0
    for i in range(len(bitblock)-1):
        if bitblock[i] != bitblock[i + 1]:
            runacc += 1
    return runacc + 1

def runs(bitblock):
    ones = bitblock.bit_ratio(1)
    length = len(bitblock)
    double_ones = 2 * length * ones * (1 - ones)
    runs = run_count(bitblock)
    return erfc((abs(runs - double_ones) / (sqrt(2 * 1/length) * double_ones)))

def israndom(pvalue):
    if pvalue < 0.01:
        return True
    else:
        return False

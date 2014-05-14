#! ../environment/bin/python3.3

#Determines whether the length of the longest run of ones is 
#consistent with the longest run expected in a random sequence."""

from bitdata import BitBlock, partition_bits, swap_bit
from scipy.stats import chi2

def bitlength(bitblocks):
    return sum([len(block) for block in bitblocks])

def prepare_bitblocks(bitstring):
    tempblock = BitBlock(bitstring)
    B, N, _ = BNKlookup(len(tempblock))
    return partition_bits(tempblock[:N*B], B)

def longest_run(bitblock, bit=1):
    """Returns the longest uninterrupted sequence of 'bit' in 
    'bitblock'"""
    start   = 0
    end     = 0
    longest = 0
    bit = swap_bit(bit)
    while end <= len(bitblock):
        try:
            end += (bitblock[start:] + [0]).index(bit)
            if  longest < end - start:
                longest = end - start
        except(ValueError):
            break
        finally:
            end += 1
            start = end
    return longest

def BNKlookup(bitcount):
    """For a given number of bits, 'N' blocks of length 'B' must be taken. 
    A value 'K' is used for calculating the P-value. These are given as 
    the tuple (B, N, K)."""
    if 128 <= bitcount < 6272:
        return (8, 16,3)
    elif 6272 <= bitcount < 750000:
        return (128, 49,5)
    elif 750000 <= bitcount: 
        return (10000, 75,6)
    else:
        print('Cannot deal with this number of bits', bitcount)
        raise ValueError

def theor_prob(K):
    if K == 3:
        return [0.2148, 0.3672, 0.2305, 0.1875]
    if K == 5:
        return [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    if K == 6:
        return [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

class Vtable():
    def __init__(self, bitcount):
        self.vkey = {i : ' is False' for i in range(7)}
        self.vstore = {i : 0 for i in range(7)}
        blocksize, _, _ = BNKlookup(bitcount)
        if blocksize == 8:
            self.vkey[0] = '<= 1'
            self.vkey[1] = '== 2'
            self.vkey[2] = '== 3'
            self.vkey[3] = '>= 4'
        elif blocksize == 128: 
            self.vkey[0] = '<= 4'
            self.vkey[1] = '== 5'
            self.vkey[2] = '== 6'
            self.vkey[3] = '== 7'
            self.vkey[4] = '== 8'
            self.vkey[5] = '>= 9'
        elif blocksize == 10000: 
            self.vkey[0] = '<= 10'
            self.vkey[1] = '== 11'
            self.vkey[2] = '== 12'
            self.vkey[3] = '== 13'
            self.vkey[4] = '== 14'
            self.vkey[5] = '== 15'
            self.vkey[6] = '>= 16'

    def classify(self, runcount):
        for idx, comparison in self.vkey.items():
            if eval(str(runcount) + comparison):
                self.vstore[idx] += 1
                break

def chi_squared(bitblocks):
    chi = 0
    _, N, K = BNKlookup(bitlength(bitblocks))
    vtable = tabulate_runcounts(bitblocks)
    prob = theor_prob(K)
    for i in range(K + 1):
        chi_numerator = (vtable.vstore[i] - N*prob[i])**2
        chi += chi_numerator / (N*prob[i])
    return chi
    
def tabulate_runcounts(bitblocks):
    bitcount = bitlength(bitblocks)
    B,_,_ = BNKlookup(bitcount)
    runtable = Vtable(bitcount)
    for block in bitblocks:
        runcount = longest_run(block)
        runtable.classify(runcount)
    return runtable

def block_runs(bitblocks):
    bitblocks = prepare_bitblocks(bitblocks)
    try:
        B, _, K = BNKlookup(bitlength(bitblocks))
    except(IndexError):
        print("Tried (and failed) to count runs in a set that is less than 128 elements.")
    else:
        chi = chi_squared(bitblocks)
        return 1 - chi2.cdf(chi, K)

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

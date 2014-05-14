#! ../environment/bin/python3.3

#This test calculates the length of the smallest linear-feedback 
#register to estimate complextiy, and decides whether 
#the sequence is likely to be random. This is based on the idea
#that a random sequence is unlikely to have a short linear-feeback
#register.

from scipy.stats import chi2
from numpy import sum
from bitdata import partition_bits

def shortest_reg(bits):
    """This is an implementation of the Berlekamp-Massey algorithm
    for binary sequences that returns the shortest linear-feedback
    register that can generate this sequence"""
    n = len(bits)
    b = [1] + [0 for i in range(n - 1)]
    c = b[:]
    L = 0
    m = -1
    for N in range(n):
        d = sum([c[i]*bits[N-i] for i in range(L+1)]) % 2
        if d != 0:
            t = c[:]
            c[N-m:] = [(c[i] != b[i-N+m]) for i in range(N-m,n)]
            if L <= N/2:
                L = N + 1 -L
                m = N
                b = t
    return L

def theor_mean(bksz):
    """The theoretical mean under an assumption of randomness"""
    return bksz / 2 + (9 + (-1)**(bksz + 1)) / 36 - (bksz / 3 + 2/9) / 2**bksz

def tabulate(blocks):
    """Used in computing the test statistic. Assumes that all blocks are of the same size,
    if they are not it will produce a meaningless result without raising an error."""
    tab = {i:0 for i in range(7)}
    bksz = len(blocks[0])
    mean = theor_mean(bksz)
    for block in blocks:
        bkm = shortest_reg(block)
        T = (-1)**bksz * (bkm - mean) + 2/9
        if T <= -2.5:
            tab[0] += 1
        elif T > 2.5:
            tab[6] += 1
        else:
            for i in range(1,6):
                if  (i - 3.5) < T <= (i - 2.5):
                    tab[i] += 1
                    break
    return tab

def theor_prob():
    """These are given in the NIST manual."""
    return [0.010417, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]

def linear_complexity(block, bksz=1000):
    blocks = partition_bits(block, bksz)
    prob = theor_prob()
    tab = tabulate(blocks)
    chisq = sum([((tab[i] - bksz * prob[i])**2) / (bksz * prob[i]) for i in range(7)])
    return 1 - chi2.cdf(chisq, 6)

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

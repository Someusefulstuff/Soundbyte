#! ../environment/bin/python3.3

#This test looks at the number of cycles having exactly K visits 
#in a cumulative sum random walk. A cycle consists of a sequence 
#of steps of unit length taken at random that begin at and return 
#to the origin. The idea is that a random sequence will not 
#continually revisit a particular state in any given cycle.

from statistics.serial_test import fqs
from statistics.template_matching import window_vwr
from scipy.stats import chi2
from numpy import sqrt, abs, sum
from math import erfc

def psums(bits):
    psum = [0]
    acc = 0
    for bit in bits:
        acc +=  bit
        psum += [acc]
    return psum + [0]

def cycles(bits, lim):
    k = -1
    cycles = {}
    walk = window_vwr(psums(bits), 2).view
    for pos in walk:
        try:
            if pos[0] == 0 and pos[1] != 0:
                k += 1
                cycles[k] = {i:0 for i in range(-lim, lim + 1) if i != 0}
            elif pos[0] != 0 and abs(pos[0]) <= lim:
                cycles[k][pos[0]] += 1
        except(IndexError):
            break
    return cycles

def theor_probs():
    """The theoretical probability that a state x occurs k
    times in a random distribution."""
    return {(-4,0) : 0.5000, (-4,1) : 0.2500, (-4,2) : 0.1250,
            (-4,3) : 0.0625, (-4,4) : 0.0312, (-4,5) : 0.0312,
            (-3,0) : 0.7500, (-3,1) : 0.0625, (-3,2) : 0.0469,
            (-3,3) : 0.0352, (-3,4) : 0.0264, (-3,5) : 0.0791,
            (-2,0) : 0.8333, (-2,1) : 0.0278, (-2,3) : 0.0231,
            (-2,3) : 0.0193, (-2,4) : 0.0161, (-2,5) : 0.0804,
            (-1,0) : 0.8750, (-1,1) : 0.0156, (-1,2) : 0.0137,
            (-1,3) : 0.0120, (-1,4) : 0.0105, (-1,5) : 0.0733,
            (1 ,0) : 0.9000, (1 ,1) : 0.0100, (1 ,2) : 0.0090,
            (1 ,3) : 0.0081, (1 ,4) : 0.0073, (1 ,5) : 0.0656,
            (2 ,0) : 0.9167, (2 ,1) : 0.0069, (2 ,2) : 0.0064,
            (2 ,3) : 0.0058, (2 ,4) : 0.0053, (2 ,5) : 0.0588,
            (3 ,0) : 0.9286, (3 ,1) : 0.0051, (3 ,2) : 0.0047,
            (3 ,3) : 0.0044, (3 ,4) : 0.0041, (3 ,5) : 0.0531}

def probs(x, k):
    if k==0:
        return 1-1.0/(2*abs(x))
    elif k>=5:
        return (1.0/(2*abs(x)))*(1-1.0/(2*abs(x)))**4
    else:
        return (1.0/(4*x*x))*(1-1.0/(2*abs(x)))**(k-1)

def freqs(cycs, lim):
    fqs = {x:0 for x in range(-lim, lim + 1) if x != 0}
    for x in fqs:
        fqs[x] = {k:0 for k in range(6)}
        for cyc in cycs:
            if cycs[cyc][x] >= 5:
                fqs[x][5] += 1
            else:
                fqs[x][cycs[cyc][x]] += 1
    return fqs
    
def random_excursions(bits):
    cycs = cycles(bits.transform_bit(0, -1), 4)
    C = len(cycs)
    chis = []
    fqs = freqs(cycs, 4)
    for x in fqs:
        chi = 0
        for k in fqs[x]:
            chi += (fqs[x][k] - C * probs(x, k))**2 / (C * probs(x, k))
        chis += [chi]
    return [1 - chi2.cdf(chi, 5) for chi in chis]

def random_excursions_variant(bits):
    bits = bits.transform_bit(0, -1)
    C = len(cycles(bits, 0))
    ps = psums(bits)
    freq = {}
    for x in ps:
        try:
            if abs(x) > 9:
                pass
            else:
                freq[x] +=1
        except(KeyError):
            freq[x] = 1
    #freq = {y:len([x for x in ps if x == y]) for y in set(ps)} 
    if 0 in freq:
        del freq[0]
    pvals = []
    for x in freq:
        pvals += [erfc((abs(freq[x] - C)) / sqrt(2 * C * (4 * abs(x) - 2)))]
    return pvals

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

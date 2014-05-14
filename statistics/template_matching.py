#! ../environment/bin/python3.3

#A template matching test slides an window of 'M' bits 
#over the bit sequence looking for template matches.
#Whenever one is found this is recorded as a hit.
#The reasoning behind this test is that too many 
#occurrences of a non-periodic pattern hints that the 
#sequence is not random.

from bitdata import partition_bits
from scipy.stats import chi2
from scipy.special import hyp1f1
from numpy import exp

def maketemplate(length):
    return [0 for i in range(length-1)] + [1]

def find_matches(block, template, skip=True):
    matches = 0
    wndwsize = len(template)
    viewer = window_vwr(block, wndwsize)
    nxtwdw = viewer.view.__next__
    while True:
        try:
            x = nxtwdw()
            if x == template:
                matches += 1
                if skip == True:
                    viewer.skip()
        except(StopIteration):
                break
    return matches

class window_vwr:
    """Provides a view onto the block, which can be compared 
    against a template."""
    def __init__(self, block, wndwsize):
        self.bk = block
        bksz = len(block)
        self.wnsz = wndwsize
        self.view = self.makegen(bksz)
    def makegen(self, bksz):
        for i in range(bksz):
            yield self.bk[i : i+self.wnsz]
    def skip(self):
        for i in range(self.wnsz - 1):
            self.view.__next__()
         
def NOTM(bits, blocksize=110000, tmpltsz=9):
    template = maketemplate(tmpltsz)
    blocks = partition_bits(bits, blocksize)
    binpow = 1/2**tmpltsz
    theor_mean = binpow*(blocksize - tmpltsz + 1)
    theor_var = blocksize*(binpow - binpow**2*(2*tmpltsz - 1))
    chi = 0
    for block in blocks:
        chi += (find_matches(block, template) - theor_mean)**2 / theor_var
    return 1 - chi2.cdf(chi, 2)

def theor_prob():
    return [0.364091, 0.185659, 0.139381, 0.100571, 0.070432, 0.139865]

def occurrences(matchings, value):
    """Moves through an array containing template matchings and returns the number of times 'value' was found."""
    return len([x for x in matchings if x == value])
    
def OTM(bits, blocksize=110000, tmpltsz=9):
    template = maketemplate(tmpltsz)
    blocks = partition_bits(bits, blocksize)
    matchings = []
    for block in blocks:
        matchings.append(find_matches(block, template, False))
    blockcount = len(blocks)
    binpow = 1/2**tmpltsz
    theor_mean = binpow*(blocksize - tmpltsz + 1)
    chi = 0
    prob = theor_prob()
    for i in range(max(matchings)+1):
        occ = occurrences(matchings, i)
        chi+= (occ - blockcount*prob[i])**2 / (blockcount * prob[i])
    return 1 - chi2.cdf(chi, max(matchings)+1)

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

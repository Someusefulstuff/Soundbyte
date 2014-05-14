#! ../environment/bin/python3.3

#This test uses a discrete fourier transform to measure the peak 
#heights. The idea is that a non-random sequence will have more 
#periodic features than a random sequence. This will be apparent
#if a majority of the peaks are significantly larger than the
#mean wave height.

from scipy.fftpack import fft
from math import sqrt, erfc

def peak_heights(bitblock):
    """Returns a sequence of half the peak heights of the 
    discrete fourier transform"""
    ftlist = fft(bitblock.transform_bit(0,-1))
    ftlength = len(ftlist)
    return abs(ftlist)[1:ftlength/2+1]

def peak_thresh(bitblock):
    """Calculates the theoretical 95% peak height threshold 
    in a random bit sequence given the number of bits"""
    bitlength = len(bitblock)
    return sqrt(2.995732274 * bitlength)

def theor_hyperthresh(bitblock):
    """The theoretical number of peaks below the threshold, 
    if the sequence is random"""
    bitlength = len(bitblock)
    threshold = peak_thresh(bitblock)
    return 0.95 * bitlength / 2

def act_hyperthresh(bitblock):
    """The actual number of peaks above the threshold, 
    if the sequence is random"""
    threshold = peak_thresh(bitblock)
    peaks = peak_heights(bitblock)
    return len([p for p in peaks if p < threshold])

def compare_hyperthresh(bitblock):
    act = act_hyperthresh(bitblock)
    theor = theor_hyperthresh(bitblock)
    numer = act - theor
    denom = sqrt(len(bitblock) * 0.95 * 0.05) / 2
    return numer / denom
    
def spectral_test(bitblock):
    return erfc(abs(compare_hyperthresh(bitblock) / sqrt(2)))

def israndom(pvalue):
    if pvalue < 0.01:
        return False
    else:
        return True

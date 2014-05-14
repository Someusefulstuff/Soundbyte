#! ./environment/bin/python3.3

#This module is used for testing the correctness of the tests.

####################################################
#Import procedures
####################################################
from bitdata import BitBlock, partition_bits

from statistics.frequency import mono_frequency
from statistics.frequency import block_frequency
from statistics.runs import runs
from statistics.block_runs import block_runs
from statistics.binary_matrix import bin_mat_rank
from statistics.spectral_test import spectral_test
from statistics.template_matching import NOTM, OTM
from statistics.maurers_test import maurers_test
from statistics.linear_complexity import linear_complexity
from statistics.serial_test import serial_test
from statistics.approximate_entropy import entropy_test
from statistics.cusum import cusum
from statistics.random_excursions import random_excursions
from statistics.random_excursions import random_excursions_variant
from statistics.testblock import testblock
                                          
####################################################
#Initialise test values
####################################################

bits100 = BitBlock("1100100100001111110110101010001"
                   "00010000101101000110000100011010"
                   "01100010011000110011000101000101"
                   "11000")
bits128 = BitBlock("11001100000101010110110001001100"
                   "11100000000000100100110101010001"
                   "00010011110101101000000011010111"
                   "11001100111001101101100010110010")
bits20a = BitBlock("01011001001010101101")
bits100a = BitBlock("11001001000011111101101010100010"
		   "00100001011010001100001000110100"
		   "11000100110001100110001010001011"
		   "1000")
bits50 = BitBlock("10111011110010110110011100101110"
                  "111110000101101001")
bits20c = BitBlock("01011010011101010111")
bits20d = BitBlock("10100100101110010110")
bits13 = BitBlock("1101011110001")
bits10b = BitBlock("0011011101")
bits12a = BitBlock("010011010101")
bits10c = BitBlock("1011010111")
bits10d = BitBlock("0110110101")
bits50  = BitBlock("10111011110010110110011100101110111110000101101001")
bits10x5e = BitBlock(testblock[:100000])
bits10x6e = BitBlock(testblock[:1000000])

####################################################
#Initialise result values
####################################################
fqmono = 0.109599
fqblock = 0.616305
runsmono = 0.500798
runsblock =  0.180598
binmat = 0.532069
notm = 0.344154
otm = 0.274932
spectral = 0.6463552
maurer = 0.767189
linecomp = 0.845406
serial = [0.843764, 0.561915]
entropy = 0.235301
cusump = 0.219194
randomwalk = [0.573306, 0.197996, 0.164011, 0.007779, 0.778616,
              0.365752, 0.790853, 0.792378]

####################################################
#Run tests
####################################################
def passfail(pvalue, comparison):
    try:
        if abs(pvalue - comparison) < 0.0001:
            return "Pass"
        else:
            return "Failed. expected = " + str(comparison) + """
                            result   = """ + str(pvalue)
    except(TypeError):
        return [passfail(pval, comparison[i]) for i, pval in enumerate(pvalue)]

def main():
    print("Frequency (monobit) test", passfail(mono_frequency(bits100), 
                                               fqmono))
    print("Frequency (block) test", passfail(block_frequency(bits100, 10),
                                             fqblock))
    print("Runs (mono) test", passfail(runs(bits100),
                                       runsmono))
    print("Runs (block) test", passfail(block_runs(bits128),
                                        runsblock))
   # print("Binary matrix rank", passfail(bin_mat_rank(bits10x5e),
   #                                      binmat))
    print("NOTM test", passfail(NOTM(bits20d,10,3),
                                         notm))
    print("OTM test", passfail(OTM(bits50,10,2),
                                         otm))
    print("Spectral test", passfail(spectral_test(bits100a,),
                                         spectral))
    print("Maurer's test", passfail(maurers_test(bits20c, 2, 4),
                                         maurer))
    #print("Linear complexity", passfail(linear_complexity(bits10x6e, 1000),
    #                                    linecomp))
    #print("Serial test", passfail(serial_test(bits10x6e, 2),
    #                                     serial))
    print("Approximate entropy test", passfail(entropy_test(bits100, 2),
                                         entropy))
    print("Cumulative sum test", passfail(cusum(bits100),
                                         cusump))
    #print("Random walk", passfail(random_excursions(bits10x6e),
    #                                     randomwalk))
    print("Random walk variant", passfail(random_excursions_variant(bits10x6e),
                                         randomwalk))
if __name__ == '__main__':
    main()

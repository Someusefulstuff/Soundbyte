#Uses the same bitstring that Charmaine Kelly used so procedures 
#can be tested against the examples

import bitdata

with open("/home/casual/Documents/PhysicsFoundation/PhyProject/Soundbyte/statistics/bin.txt",'r') as binfile:
    testblock = bitdata.BitBlock(binfile.read())

#! ../environment/bin/python3.3

import argparse
import os

def main():
    parser = argparse.ArgumentParser(description = 'Reads binary data from a file')
    parser.add_argument('-i, --in',
                        type = str,
                        default = '/dev/dsp',
                        help = 'Specifies file to read.',
                        dest = 'datasource')
    parser.add_argument('-d, --debias',
                        default = False,
                        const = True,
                        action = 'store_const',
                        help = 'Uses Von Neumann algorithm to balance numbers of 1s and 0s',
                        dest = 'debias')
    parser.add_argument('output',
                        type = str,
                        help = 'Specifies file to write to.')

    opts = parser.parse_args()
    BitSource = DataStream(opts.datasource)
    bitpr = [0,0]
    out = open(opts.output,'w')
    while True:
        bitpr = BitSource.getBits()
        if len(bitpr) != 2:
            break
        if opts.debias == True:
            out.write(VNdebias(bitpr))
        else:
            out.write(bitpr)
    out.close()

def VNdebias(bits):
    if bits[0] == bits[1]:
        return ''
    else:
        return bits[1]

class DataStream:
    def __init__(self, datasource):
        self.datasource = datasource
        self.stream = self.byteSet()
    def byteSet(self, size=2):
        with open(self.datasource,'rb') as bitSource: 
            while True:
                yield bitSource.read(size)
    def getBits(self):
        """Gives the two 8th bits from the next byte pair."""
        byts = self.stream.__next__()
        return ''.join([bits[7] for bits in [format(byt,'08b') for byt in byts]])

if __name__ == "__main__":
    main()

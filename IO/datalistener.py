#! ../environment/bin/python3.3

import argparse
import tempfile
import os
from itertools import tee
from binascii import hexlify

def main():
    parser = argparse.ArgumentParser(description = 'Reads binary data from a file')
    parser.add_argument('-f, --file',
                        type = str,
                        default = '/dev/dsp',
                        help = 'Specifies file to read.',
                        dest = 'datasource')
    parser.add_argument('-b, --bytesize',
                        type = int,
                        default = None,
                        help = 'Specifies number of bytes to read.',
                        dest = 'bytesize')
    parser.add_argument('-d, --debias',
                        default = False,
                        const = True,
                        action = 'store_const',
                        help = 'Uses Von Neumann algorithm to balance numbers of 1s and 0s',
                        dest = 'debias')
    parser.add_argument('-t, --temp',
                        default = '/tmp',
                        help = 'Give a prefix destination for storing temporary files',
                        dest = 'temp')

    opts = parser.parse_args()
    BitSource = DataStream(opts.datasource)
    print(BitSource.getBinary(opts.bytesize, opts.debias, opts.temp))

def VNdebias(binary, temp):
    debfile = tempfile.TemporaryFile(mode='a+', prefix = temp)
    while True:
        bits = binary.read(2)
        try:
            if bits[0] != bits[1]: 
                debfile.write(bits[1])
        except(IndexError):
            break
    debfile.seek(0)
    return debfile.read()

class DataStream:
    def __init__(self, datasource):
        self.datasource = datasource
    def getBytes(self, bytesize):
        with open(self.datasource,'rb') as bitSource: 
            return bitSource.read(bytesize)
    def getInts(self, bytesize):
        sourcebytes = self.getBytes(bytesize)
        return sourcebytes
    def getBinary(self, bytesize, debias, temp):
        binfile = tempfile.TemporaryFile(mode='w+', prefix=temp)
        for bit in self.getInts(bytesize):
            binfile.write(format(bit,'08b'))
        binfile.seek(0)
        if debias == False:
            return binfile.read()
        else:
            return VNdebias(binfile, temp)

if __name__ == "__main__":
    main()

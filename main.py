#! environment/bin/python3.3

#This module runs statistical tests on binary data and outputs the results.

from bitdata import BitBlock, partition_bits
from os.path import basename
from sympy.core.cache import clear_cache
import sqlite3

from statistics.frequency import mono_frequency, block_frequency
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
from statistics.random_excursions import random_excursions, random_excursions_variant

testparams =  [(mono_frequency   , 100    ), (block_frequency  , 2000   ), (runs             , 100    ),
               (block_runs       , 128    ), (bin_mat_rank     , 100000 ), (spectral_test    , 1024   ),
               (maurers_test     , 387840 ), (linear_complexity, 1000000), (serial_test      , 500    ), 
               (entropy_test     , 500    ), (cusum            , 100    ), (random_excursions, 1000000), 
               (random_excursions_variant, 1000000)]

wd = '/home/casual/Documents/PhysicsFoundation/PhyProject/Soundbyte/IO/processed/'
files =  [wd + 'nosig.txt', 
          wd + 'sine100.txt', 
          wd + 'sine50.txt',
          wd + 'sine1.txt',
          wd + 'sine0.1.txt',
          wd + 'square100.txt',
          wd + '98.1.txt']

class DripFeeder:
    """Holds a generator that allows a file to be read in bitesized chunks"""
    def __init__(self, dropsize, filepath):
        self.dripper = self.makegen(dropsize, filepath)
        self.dripno = 0
    def drip(self):
        self.dripno += 1
        return self.dripper.__next__()
    def makegen(self, dropsize, filepath):
        with open(filepath, 'r') as f:
            while True:
                yield BitBlock(f.read(dropsize))

def sprinkler(dropsize, files):
    spkr = {}
    for f in files:
        spkr[basename(f)] = DripFeeder(dropsize, f)
    return spkr

class DB:
    def __init__(self, name='RandTestResults.db'):
        self.conn = sqlite3.connect(name)
        self.curs = self.conn.cursor()
        self.curs.execute('CREATE TABLE IF NOT EXISTS results '
                          '(dripNo INTEGER, filename TEXT, '
                          'testname TEXT, testNo INTEGER, pvalue REAL)')
    def store(self, dripno, fname, tname, testno, pvalue):
        print('>    Got p-value:', pvalue, '\n')
        self.curs.execute('INSERT INTO results '
                          'VALUES (?,?,?,?,?) ', 
                          [dripno, fname, tname, testno, pvalue])
        self.conn.commit()
    def hasresult(self, dripno, fname, tname):
        crit = ('dripNo = '  + "'" + str(dripno) + "'" + ' AND '
                'filename =' + "'" + fname      + "'"  + ' AND '
                'testname =' + "'" + tname      + "'")
        self.curs.execute('SELECT 1 from results WHERE ' + crit)
        if self.curs.fetchone():
            return True
        else:
            return False
#Write something to check if a test has already been performed.

def remfails(fails):
    for (fail, datasrc) in fails:
        try:
            del datasrc[fail]
        except(KeyError):
            pass


def main(results):
    testholder = []
    for (test, dropsize) in testparams:
        datasrc = sprinkler(dropsize, files)
        testholder += [(test, datasrc)]
    failcount = 0
    while failcount != len(testparams) * len(files):
        for (test, datasrc) in testholder:
            fails = []
            for (fname, Drip) in datasrc.items():
                block = Drip.drip()
                if block == []:
                    fails += [(fname, datasrc)]
                    failcount += 1
                else:
                    print('Testing', fname, 'with', test.__name__, 'drip no.', Drip.dripno)
                    if not results.hasresult(Drip.dripno, fname, test.__name__):
                        while True:
                            try:
                                pvalue = test(block)
                                break
                            except(MemoryError):
                                clear_cache()
                        try:
                            for i, pval in enumerate(pvalue):
                                results.store(Drip.dripno, fname, test.__name__, i, pval)
                        except(TypeError):
                            results.store(Drip.dripno, fname, test.__name__, 1, pvalue)
            remfails(fails)

if __name__ == '__main__':
    results = DB()
    try:
        main(results)
    except(KeyboardInterrupt):
        results.curs.close()
        results.conn.close()

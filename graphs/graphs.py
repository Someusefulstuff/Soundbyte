#! ../environment/bin/python3.3
#Prepares graphs for the research documentation.

import matplotlib.pyplot as plt
import sqlite3
from os.path import splitext

nicefile = {'sine100.txt'  : 'Sine 100 %'  ,
            'sine50.txt'   : 'Sine 50 %'   ,
            'sine1.txt'    : 'Sine 1 %'    ,
            'sine0.1.txt'  : 'Sine 0.1 %'  ,
            'nosig.txt'    : 'No signal'   ,
            'square100.txt': 'Square 100 %',
            '98.1.txt'     : '98.1MHz'      }

nicetest = {'bin_mat_rank'              : 'Binary matrix rank',
            'block_frequency'           : 'Frequency (Block)',
            'block_runs'                : 'Longest run of ones in a block',
            'cusum'                     : 'Cumulative sums',
            'entropy_test'              : 'Approximate entropy',
            'linear_complexity'         : 'Linear complexity',
            'maurers_test'              : 'Maurers universal statistic',
            'mono_frequency'            : 'Frequency (Monobit)',
            'random_excursions'         : 'Random excursions',
            'random_excursions_variant' : 'Random excursions variant',
            'runs'                      : 'Runs test',
            'serial_test'               : 'Serial test',
            'spectral_test'             : 'Discrete fourier transform (spectral)'}
def main():
    try:
        conn = sqlite3.connect('../RandTestResults.db')
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT filename, testname '
                    'FROM results '
                    'ORDER BY dripno ASC;')
        tests = cur.fetchall()
        for src, test in tests:
            cur.execute("SELECT pvalue "
                        "FROM results "
                        "WHERE filename = '" + src  + "' "
                        "AND   testname = '" + test + "';")
            pvals = cur.fetchall()
            pvals = [pval[0] for pval in pvals]
            print('Graphing', nicetest[test], 'on', nicefile[src])
            plt.bar(range(len(pvals)), pvals)
            plt.title(splitext(nicefile[src])[0] + ' ' + nicetest[test])
            plt.savefig(splitext(src)[0] + '_' + test + '.png')
            plt.clf()
    except(KeyboardInterrupt, Exception):
        return 1
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    main()

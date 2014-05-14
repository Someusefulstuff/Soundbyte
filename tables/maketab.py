#! ../environment/bin/python3.3

import sqlite3
from prettytable import from_db_cursor as db_src

nicefile = {'sine100.txt'  : 'Sine 100\%'  ,
            'sine50.txt'   : 'Sine 50\%'   ,
            'sine1.txt'    : 'Sine 1\%'    ,
            'sine0.1.txt'  : 'Sine 0.1\%'  ,
            'nosig.txt'    : 'No signal'   ,
            'square100.txt': 'Square 100\%',
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
conn = sqlite3.connect('../RandTestResults.db')
curs = conn.cursor()

#Mean
curs.execute('SELECT testname, filename, round(avg(pvalue),2) AS avgpval '
             'FROM results '
             'GROUP BY testname, filename '
             'ORDER BY filename, testname')
with open('averages.txt', 'w') as f:
    f.write(db_src(curs).get_string())
curs.execute('SELECT testname, filename, round(avg(pvalue),2) AS avgpval '
             'FROM results '
             'GROUP BY testname, filename '
             'ORDER BY filename, testname')
with open('averages.tex', 'w') as f:
    for x, y, z in curs.fetchall():
        f.write(nicetest[x] + ' & ' + ' & '.join([nicefile[y], str(z)]) + r' \\ ' + '\n ')

#Random_pass
curs.execute('SELECT tabA.testname, tabA.filename, randompass, testcount, '
             'round((100.0*randompass/testcount), 2) AS pcntpass '
             'FROM ( '
                     'SELECT testname, filename, count(pvalue) AS randompass, pvalue >= 0.01 AS is_random '
                     'FROM results '
                     'WHERE is_random = 1 '
                     'GROUP BY testname, filename, is_random '
                  ') as tabA '
             'JOIN '
                  '( ' 
                     'SELECT testname, filename, count(pvalue) as testcount '
                     'FROM results '
                     'GROUP BY testname, filename '
                  ') as tabB '
                 'ON tabA.testname = tabB.testname AND tabA.filename = tabB.filename '
                 'ORDER BY tabA.filename, tabA.testname;') 
with open('israndom.txt', 'w') as f:
    f.write(db_src(curs).get_string())
curs.execute('SELECT tabA.testname, tabA.filename, '
             'round((100.0*randompass/testcount), 2) AS pcntpass '
             'FROM ( '
                     'SELECT testname, filename, count(pvalue) AS randompass, pvalue >= 0.01 AS is_random '
                     'FROM results '
                     'WHERE is_random = 1 '
                     'GROUP BY testname, filename, is_random '
                  ') as tabA '
             'JOIN '
                  '( ' 
                     'SELECT testname, filename, count(pvalue) as testcount '
                     'FROM results '
                     'GROUP BY testname, filename '
                  ') as tabB '
                 'ON tabA.testname = tabB.testname AND tabA.filename = tabB.filename '
                 'ORDER BY tabA.filename, tabA.testname;') 
with open('israndom.tex', 'w') as f:
    for x, y, z in curs.fetchall():
        f.write(nicetest[x] + ' & ' + ' & '.join([nicefile[y], str(z)]) + r' \\ ' + '\n ')

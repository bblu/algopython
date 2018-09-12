# -*- coding: utf-8 -*-
# python3 by bblu for csv

import sys
from os import listdir
import pandas as pd

def rename(zhan, xiao, text):
    # for float('nan')
    if text != text:
        return text
    mult = text.split(',')
    if len(mult) > 1:
        txt = ''
        for i in mult:
            txt += rename(zhan, xiao, i) + ','
        return txt[:-1]
    if text.startswith(u'二'):
        return zhan + text
    if text[0] == zhan[0]:
        return text;
    return xiao + text

def refile(filename):
    df = pd.read_csv(filename, encoding='gbk')
    dt = open(filename.replace('.','_.'),'w')
    dt.write(','.join(df.columns)+'\n')

    r0 = df.values[0]
    bian = r0[0]
    zhan = r0[1]
    xiao = r0[2]
    idxn, idxl = 6,8
    if bian.find('-GX') > 7:
        idxn, idxl = 7,8
    elif bian.find('-FMJ') > 7:
        idxn, idxl = 5,-1

    c = 0
    for row in df.values:
        c += 1
        print(c, row[:idxl])
        name = row[idxn]
        row[idxn] = rename(zhan,xiao,name)
        if idxl > 0:
            link = row[idxl]
            row[idxl] = rename(zhan,xiao,link)
        line = ''
        for r in row:
            r = str(r)
            if r.find(',') > 0:
                line += '"' + str(r) + '",'
            elif r=='nan':
                line += ' ,'
            else: 
                line += r + ','
        line = line[:-1] + '\n'
        dt.write(line)
        #if c == 10:
        #    break

    dt.close()

for f in listdir('.'):
    if f.endswith('.csv'):
        print(f)
        refile(f)



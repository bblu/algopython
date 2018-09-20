# -*- coding: utf-8 -*-
# python3 by bblu for csv

import sys
from os import listdir
import pandas as pd

def rename(zhan, xiao, text, sepa):
    # for float('nan')
    if text != text:
        return text
    mult = text.split(sepa)
    if len(mult) > 1:
        txt = ''
        for i in mult:
            if i != '':
                txt += rename(zhan, xiao, i, sepa) + sepa
        #print('mult:',mult,txt)
        return txt[:-1]
    if text.startswith(u'二'):
        return zhan + text
    #print('--------------',text,zhan)
    if text[0] == zhan[0]:
        return text;
    return xiao + text

def refile(filename):
    #df = pd.read_csv(open(filename, encoding='gbk'))
    df = pd.read_csv(open(filename, encoding='utf-8'))
    dt = open(filename.replace('.','-2386.'),'w')
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

    c = 1
    e = 0
    for row in df.values:
        c += 1
        if row[0] != row[0]:
            print(c,'*** Error:*** No Data')
            break
        if row[0].startswith('DDS-'):
            pass
        elif row[0].startswith('DD-'):
            row[0] = row[0].replace('DD-','DDS-')
        else:
            row[0] = 'DDS-'+row[0]
        if idxn == 5:
            pass
        elif idxn == 7 and len(row[5])==2:
            row[5]= '二次网%s管'%row[5]
        # Node
        elif idxn == 6:
            if row[3]==row[3] and ord(row[3][0])>48 and ord(row[3][0])<58:
                row[3] = row[2]+row[3]

            if row[4]==row[5]:
                row[5]= '普通'+row[5]
            elif row[5].startswith('支线'):
                print('----------=* warn *=----------[',c , ']',row[5])
                row[5]=row[5][2:]
        
        name,link = row[idxn],''
        row[idxn] = rename(zhan,xiao,name,'-')
        if idxl > 0:
            link = row[idxl]
            row[idxl] = rename(zhan,xiao,link,',')
        if name != row[idxn] or link != row[idxl]:
            e += 1
            print(c, '-', e , row[idxn], row[idxl])
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
        #if c == 5:
        #    break

    dt.close()

for f in listdir('.'):
    if f.endswith('-2386.csv'):
        continue
    if f.endswith('.csv'):
        print(f)
        refile(f)



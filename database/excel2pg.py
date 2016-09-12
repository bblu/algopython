#!usr/bin/python
# -*- coding: utf-8 -*-

#apt-get install python-xlrd
import xlrd
from pg import DB

import sys
type = sys.getfilesystemencoding()
print(type)

db=DB(dbname='postgres',host='localhost',port=5432,user='postgres',passwd='postgres')

xl=xlrd.open_workbook(u'电大所-海银御景站-管网.xls')
#xl=xlrd.open_workbook('/home/bblu/repo/algopython/database/pipe.xls')
sheetname = xl.sheet_names()
xl_sheet = xl.sheet_by_index(0)
print xl_sheet.name
xl_sheet1 = xl.sheet_by_name(u'Sheet1')
print xl_sheet1.name
fileds=""
for col in range(0,xl_sheet.ncols):
    fileds+=xl_sheet.cell(0,col).value+','
print(fileds)

for row in range(1,xl_sheet.nrows):
    fileds=""
    for col in range(0,xl_sheet.ncols):
        fileds+= unicode(xl_sheet.cell(row,col).value) + ','
    print(fileds)


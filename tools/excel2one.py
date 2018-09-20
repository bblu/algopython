# -*- coding:utf-8 –*-

import os
import xlrd
import xlsxwriter

def exp2one(obj):
    source_xls = os.listdir()
    target_xls = "电大所-2018-%s"%obj

    # 读取数据
    data = []
    j=0
    for i in source_xls:
        if not i.endswith(obj):
            continue
        
        wb = xlrd.open_workbook(i)
        sheet = wb.sheets()[0]
        k=0
        for rownum in range(sheet.nrows):
            if j > 0 and k == 0:
                print(sheet.row_values(rownum))
                k+=1
                continue
            data.append(sheet.row_values(rownum))
            k+=1
        j+=1
        print(j,k,i)
    #print(data)
    # 写入数据
    workbook = xlsxwriter.Workbook(target_xls)
    worksheet = workbook.add_worksheet()
    font = workbook.add_format({"font_size":10})
    for i in range(len(data)):
        for j in range(len(data[i])):
            worksheet.write(i, j, data[i][j], font)
    # 关闭文件流
    workbook.close()

objs = ['阀门井-2386.xlsx','节点-2386.xlsx','管线-2386.xlsx']
for obj in objs:
    exp2one(obj)

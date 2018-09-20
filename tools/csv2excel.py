# -*- coding:utf-8 –*-
'''
程序用来将excel批量转换为csv文件。指定源路径和目标路径。
ModuleNotFoundError: No module named 'openpyxl'
pip install openpyxl
'''

import pandas as pd
import os

#读取一个目录里面的所有文件：
def read_path(path):
    dirs=os.listdir(path)
    return dirs

#主函数
def csv2excel(src,obj):
    #将源文件路径里面的文件转换成列表file_list
    file_list=[src+i for i in read_path(src)]
    j=1
    #建立循环对于每个文件调用excel_to_csv()
    for it in file_list:
        if not it.endswith('2386.csv'):
            continue
        (shotname,extension) = os.path.splitext(it.split('\\')[-1])
        xls = obj + shotname + '.xlsx'
        print(j,it,xls)
        #OSError: Initializing from file failed=>pd.read_csv(open(file))
        data_xls=pd.read_csv(open(it))
        data_xls.to_excel(xls,index=False,sheet_name=shotname)
        
        j=j+1


if __name__ == '__main__':
    csv2excel('D:\\diandasuo_2018\\python\\','D:\\diandasuo_2018\\2018\\')

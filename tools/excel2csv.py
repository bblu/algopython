# -*- coding:utf-8 –*-
'''
程序用来将excel批量转换为csv文件。指定源路径和目标路径。
ModuleNotFoundError: No module named xlrd
>pip install xlrd
'''

#导入pandas
import pandas as pd
import os


#建立单个文件的excel转换成csv函数,file 是excel文件名，to_file 是csv文件名。
def excel_to_csv(file,to_file):
    data_xls=pd.read_excel(file,sheet_name=0)
    data_xls.to_csv(to_file,index=False)



#读取一个目录里面的所有文件：
def read_path(path):
    dirs=os.listdir(path)
    return dirs

#主函数
def main(src,obj):
    #将源文件路径里面的文件转换成列表file_list
    file_list=[src+i for i in read_path(src)]
    j=1
    #建立循环对于每个文件调用excel_to_csv()
    for it in file_list:
        csv = it.replace('.xlsx','.csv')
        csv = obj + csv.split('\\')[-1]
        print(j,it,csv)
        excel_to_csv(it,csv)
        j=j+1


if __name__ == '__main__':
    main('D:\\diandasuo_2018\\2018\\','D:\\diandasuo_2018\\python\\')

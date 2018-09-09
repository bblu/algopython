# -*- coding: utf-8 -*-
from pg import DB

db=DB(dbname='fzgis',host='localhost',port=5432,user='postgres',passwd='123456')

# 需要创建表就设为True
notInit = True

#建表sql自己写
def init(item):
    global pg
    #db.query("create table equ(equip_type character varying(5) ,item_id character varying(84),pms_equip_id character varying(84),)")

c = 0

fs = 'id,shape,equip'
for line in open('./equ.csv', 'r').readlines():
    item = line[:-1].split(',')
    #print item
    if notInit:
        init(item)
        notInit = False
        continue
    vs = "'%s', '%s', '%s'" % ( item[4],item[5],item[-1][:-1])
    #print vs
    sql = 'insert into equ values(%s)'%(vs)
    print sql
    #break
    db.query(sql)
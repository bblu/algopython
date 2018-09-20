.# -*- coding:utf-8 –*-
import json
import pandas as pd
from pg import DB

#'LINESTRING(-72.1260 42.45, -72.123 42.1546)'

pgcnn=DB(dbname='sggis',host='localhost',port=5433,user='postgres',passwd='123456')

def getPts(pt):
    return pt[1:-1].replace(',',' ')

sql = 'select bh,qdzb,zdzb from pipe'
columns = pgcnn.query(sql).namedresult()
for col in columns:
    p0 = col.qdzb
    p1 = col.zdzb
    pt = '%s,%s' % (getPts(p0),getPts(p1))
    sql = "update pipe set geometry =ST_Transform(ST_GeomFromText('LINESTRING(%s)', 2386),4326) where bh='%s'"%(pt,col.bh)
    #print(sql)
    #break
    pgcnn.query(sql)

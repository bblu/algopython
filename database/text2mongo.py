#poi GB18030
import json
import pymongo
from pg import DB

from dbconfig import *
pgcnn=DB(dbname=pgName,host=pgHost,port=pgPort,user=pgUser,passwd=pgPswd)
mgcnn=pymongo.MongoClient(mgHost,mgPort)
cndata=mgcnn.sggis.data

def genSql(tbname):
    cols='''select row_to_json(tb) as json from (
            select textid as id,stext as name,textuid,mapid,st_asgeojson(geom) as geometry,typecode
             from %s ) tb;''' % tbname
    return cols

for row in ['text']:
    tbname=row
    print(tbname)
    sql = genSql(tbname)
    print(sql)
    dts=pgcnn.query(sql).namedresult()
    c = 0
    d = 0
    for dt in dts:
        dt.json['device_table']='public.label_layer'
        geo = dt.json['geometry']
        if geo:
            dt.json['geometry']=json.loads(geo)
        dt.json['provice']='grid'
        cndata.insert(dt.json)
        c+=1
        d+=1
        if c==10000 :
            print d
            c=0
        elif c%1000 == 0:
            print d,
        
    print(d)
    

    

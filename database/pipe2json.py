# -*- coding: utf-8 -*-
import json
import pymongo
from pg import DB
#python 3
pgcnn=DB(dbname='sggis',host='localhost',port=5433,user='postgres',passwd='123456')

mgcnn=pymongo.MongoClient('192.168.111.250',27017)
cndata=mgcnn.jilin_baishan.data
#cndata.remove({'device_table':'public.road_label_layer'})

def genSql(tbname):
    global pgcnn
    sql = "select column_name,data_type from information_schema.columns where table_schema='public' and table_name = '%s'" % tbname
    columns = pgcnn.query(sql).namedresult()
    cols='select row_to_json(tb) as json from (select '
    for tup in columns:
        name = tup.column_name
        if(name!='zscale'):
            if(name == 'geometry'):
                name = 'st_asgeojson(geometry) as geometry'
            elif(name == 'wkb_geometry'):
                name = 'st_asgeojson(wkb_geometry)as geometry'
            cols+=name+','
    cols = cols.rstrip(',')
    cols += ' from %s ) tb;' % tbname
    return cols

#pgtbs=pgcnn.query("select tablename from pg_tables where schemaname='public' and tablename like 'bs_%_layer' order by tablename;")
#tbrows=pgtbs.namedresult()
tbrows=['pipe']
for row in tbrows:
    #tbname=row.tablename
    tbname=row
    print(tbname)
    sql = genSql(tbname)
    print(sql)
    dts=pgcnn.query(sql).namedresult()
    c = 0
    d = 0
    w = open('pipe.json','w')
    for dt in dts:
        dt.json['xdwz']=''
        dt.json['sccj']=''
        dt.json['sjdw']=''
        dt.json['sgdw']=''
        dt.json['wxyy']=''
        dt.json['fsfs']=u"直埋"
        dt.json['fssd']=1.5
        dt.json['bwcl']=u"聚氨酯"
        dt.json['whklx']=u"聚乙烯"
        dt.json['bz']="20180920"
        dt.json['zw_type']='597'
        dt.json['zw_subtype']='59721'
        dt.json['zw_editStatus']='add'
        dt.json['zw_jobId']='0xff7c98a2c70-dc7c-11e6-a83c-070be305ac7f'
        dt.json['device_table']='internal.4e878d95-cca7-11e6-9d41-c5407f31c5f2'
        geo = dt.json['geometry']
        if geo:
            dt.json['geometry']=json.loads(geo)
        #print(dt.json)
        w.write(json.dumps(dt.json)+'\n')
        #cndata.insert(dt.json)
        c+=1
        d+=1
        if c==10000 :
            print(d)
            c=0
        elif c%1000 == 0:
            print(d,)
    w.close()
    print(d)
    

    

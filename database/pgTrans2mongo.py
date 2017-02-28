import json
import pymongo
from pg import DB



pgcnn=DB(dbname='osm',host='localhost',port=5432,user='postgres',passwd='123456')

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
                name = 'st_asgeojson(st_transform(geometry,4326))as geometry'
            elif(name == 'wkb_geometry'):
                name = 'st_asgeojson(st_transform(wkb_geometry,4326))as geometry'
            cols+=name+','
    cols = cols.rstrip(',')
    cols += ' from %s ) tb;' % tbname
    return cols

pgtbs=pgcnn.query("select tablename from pg_tables where schemaname='public' and tablename like 'bs_%_layer' order by tablename;")
tbrows=pgtbs.namedresult()

for row in tbrows:
    tbname=row.tablename
    print(tbname)
    sql = genSql(tbname)
    print(sql)
    dts=pgcnn.query(sql).namedresult()
    c = 0
    d = 0
    for dt in dts:
        dt.json['device_table']='public.'+tbname
        geo = dt.json['geometry']
        if geo:
            dt.json['geometry']=json.loads(geo)
        cndata.insert(dt.json)
        c+=1
        d+=1
        if c==10000 :
            print d
            c=0
        elif c%1000 == 0:
            print d,
        
    print(d)
    

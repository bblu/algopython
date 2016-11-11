import json
import pymongo
from pg import DB
from pgdb import connect


pgcnn=DB(dbname='osm',host='localhost',port=5432,user='postgres',passwd='123456')
cnn=connect(dbname='osm',host='localhost:5432',user='postgres',password='123456')
cursor = cnn.cursor()
mgcnn=pymongo.MongoClient('192.168.111.250',27017)
cndata=mgcnn.china.data
#cndata.remove({'device_table':'public.water_layer'})

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
    cols += ' from %s) tb;' % tbname
    return cols

#pgtbs=pgcnn.query("select tablename from pg_tables where schemaname='public' and tablename like '%_layer' order by tablename;")
#tbrows=pgtbs.namedresult()
tbrows=['water_layer','road_label_layer','road_layer']
for row in tbrows:
    tbname=row #row.tablename
    print(tbname)
    #if tbname != 'country_label_layer':
    #    continue
    sql = genSql(tbname)
    print(sql)
    #break
    cursor.execute(sql)
    c = 0
    d = 0
    for trow in cursor:
        row = trow._asdict()['json']
        row['device_table']='public.'+tbname
        geo = row.json['geometry']
        if geo:
            row['geometry']=json.loads(geo)
        cndata.insert(row)
        c+=1
        d+=1
        if c==5000 :
            print d
            c=0
        elif c%500 == 0:
            print d,
        
    print(d)
    

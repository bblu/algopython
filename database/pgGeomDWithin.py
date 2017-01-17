import json
import pymongo
from pg import DB

pgcnn=DB(dbname='osm',host='localhost',port=5432,user='usrname',passwd='pswd')

def genSql(tbname):
    global pgcnn
    sql = "select column_name,data_type from information_schema.columns where table_schema='public' and table_name = '%s'" % tbname
    columns = pgcnn.query(sql).namedresult()
    cols='create table bs_%s AS (select ' % tbname
    geoName = 'geometry'

    for tup in columns:
        name = tup.column_name
        if(name!='zscale'):
            if(name == 'geometry'):
                name = 'st_transform(geometry,4326) as geometry'
            elif(name == 'wkb_geometry'):
                geoName = 'wkb_geometry'
                name = 'st_transform(wkb_geometry,4326) as geometry'
            cols+=name+','
    cols = cols.rstrip(',')
    cols += ' from %s where ST_DWithin(ST_GeomFromText(\'point(14073555 5151365)\',3857),%s,11500));' % (tbname,geoName)
    return cols

pgtbs=pgcnn.query("select tablename from pg_tables where schemaname='public' and tablename like '%_layer' order by tablename;")
tbrows=pgtbs.namedresult()

for row in tbrows:
    tbname = row.tablename
    print(tbname)
    #sql = 'drop table %s;'%tbname
    sql = genSql(tbname)
    print(sql)
    pgcnn.query(sql)

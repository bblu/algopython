import re
import json
import pymongo
from pg import DB
from datetime import datetime

pgcnn=DB(dbname='china',host='localhost',port=5432,user='postgres',passwd='123456')

mgcnn=pymongo.MongoClient('192.168.111.250',27017)
_start = datetime.now()
cndata=mgcnn.background.data

def genSql(tbname):
    global pgcnn,edgeid
    subsql = ''
    if tbname.startswith('roadsegment_'):
        subsql = '''select roadid as osm_id,roadname as name,routeno,mapid,st_asgeojson(st_linemerge(geom)) as geometry,
            linktype,length,roadclass,showgrade levelid,
            case 	when iftunnel = 1 then 'tunnel'
                when ifbridge = 1 then 'bridge'
		when ifsink	  = 1 then 'ford'
		when ifoverhead = 1 then 'overhead'
            end
            as structure 
            from %s where showgrade <= 5'''%tbname
    elif tbname.startswith('water'):
         subsql = '''select id as osm_id,name,st_asgeojson((st_dump(geom)).geom) as geometry,area,levelid,type typeid,orderid
            from %s where id > %s order by id'''% (tbname,edgeid)

    else:
        psql = "select column_name,data_type from information_schema.columns where table_schema='public' and table_name = '%s'" % tbname
        columns = pgcnn.query(psql).namedresult()
        subsql='select '
        for tup in columns:
            name = tup.column_name
            if name == 'geometry' or name == 'geom':
                if tbname == 'water_layer':
                    name = 'st_asgeojson((st_dump(%s)).geom) as geometry' % name
                else:
                    name = 'st_asgeojson(%s) as geometry' % name
            subsql+=name+','
        subsql = subsql.rstrip(',')
        subsql += ' from %s'% tbname

    sql ='select row_to_json(tb) as json from (%s) tb' % subsql

    
    return sql

def impData(sql,devName):
    global pgcnn
    dts=pgcnn.query(sql).namedresult()
    c = 0
    d = 0
    _start = datetime.now()
    tms = 0
    for dt in dts:
        dt.json['device_table']='public.'+ devName
        geo = dt.json['geometry']
        if geo:
            dt.json['geometry']=json.loads(geo)
        _s = datetime.now()
        cndata.insert(dt.json)
        _e = datetime.now()
        tm = _e - _s
        tms = tms + tm.microseconds
        c+=1
        d+=1
        if c==10000 :
            print d
            c=0
        elif c%1000 == 0:
            print d,
    print(d)
#pgtbs=pgcnn.query("select tablename from pg_tables where schemaname='public' and tablename like 'jilin_place_%_layer' order by tablename;")
#tbrows=pgtbs.namedresult()
#tbrows = ['jilin_landuse_layer','jilin_place_label_layer','jilin_road_layer','jilin_water_layer']
impRoad = False
tbrows = ['water']
edgeid = '633572224'
if impRoad in tbrows:
    for row in range(1,14):
        tbname='roadsegment_%s'%row
        tbrows.append(tbname)
log = open('./errorIds.log','a')
for tbname in tbrows:
    devname = tbname
    if tbname.startswith('roadsegment'):
        devname = 'road_layer'
    elif not tbname.endswith('_layer'):
        devname = tbname + '_layer'
    print 'remove %s from mongo ...'% devname
    #cndata.remove({'device_table':'public.%s'%devname})
    _end = datetime.now()
    tm = _end - _start
    print '%s removed time: %ss'% (tbname,tm.seconds)
    
    print tbname,devname
    log.write('\ntb:%s,dev:%s\n'%(tbname,devname))

    while True:
        sql = genSql(tbname)
        print(sql)
        try:
            impData(sql,devname)
        except pymongo.errors.WriteError  as e:
            p = e.message.find('osm_id:')
            if p > 0:
                eid = e.message[p:p+17]
                print 'WriteError:',eid
                edgeid = eid.split(':')[1]
                log.write(edgeid + ',')
                continue
            else:
                print e
                break
        break
    
    _end = datetime.now()
    tm = _end - _start
    print '>>>+table:%s time: %ss'% (tbname,tm.seconds)
    log.flush()

log.close()
    

    

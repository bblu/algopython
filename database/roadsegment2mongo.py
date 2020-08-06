import json
import pymongo
from pg import DB
from datetime import datetime

from dbconfig import *
pgcnn=DB(dbname=pgName,host=pgHost,port=pgPort,user=pgUser,passwd=pgPswd)
mgcnn=pymongo.MongoClient(mgHost,mgPort)
cndata=mgcnn.sggis.data

#print 'remove layer ...'
#cndata.remove({'device_table':'public.road_layer'})
#_end = datetime.now()
#tm = _end - _start
#print 'layer removed time: %ss'% tm.seconds

def genSql(tbname):
    global pgcnn
    sql = '''select row_to_json(tb) as json from (
        select roadid as id,roadname as name,routeno,mapid,st_asgeojson(st_linemerge(geom)) as geometry,
        linktype,length,roadclass,showgrade levelid,
        case 	when iftunnel = 1 then 'tunnel'
		when ifbridge = 1 then 'bridge'
		when ifsink	  = 1 then 'ford'
		when ifoverhead = 1 then 'overhead'
        end
        as structure 
        from %s where showgrade <= 5) tb'''%tbname
    return sql

for row in range(1,14):
    tbname='roadsegment_%s'%row
    print(tbname)
    sql = genSql(tbname)
    print(sql)
    dts=pgcnn.query(sql).namedresult()
    c = 0
    d = 0
    _start = datetime.now()
    tms = 0
    for dt in dts:
        dt.json['device_table']='public.road_layer'
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
    _end = datetime.now()
    tm = _end - _start
    print 'all time: %s'% tm.seconds
    tms = tms/1000000
    print 'insert time: %s'% tms
    
    

    

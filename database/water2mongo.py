import json
import pymongo
from pg import DB
from datetime import datetime


pgcnn=DB(dbname='sggis',host='192.168.1.250',port=5432,user='postgres',passwd='123456')

mgcnn=pymongo.MongoClient('192.168.1.25',27017)
_start = datetime.now()
cndata=mgcnn.china.shanxii
print 'remove layer ...'
#cndata.remove({'device_table':'public.landuse_layer'})
_end = datetime.now()
tm = _end - _start
print 'layer removed time: %ss'% tm.seconds

def genSql(tbname):
    sql = 'select row_to_json(tb) as json from (select id,bkuid,mapid,levelid,type typeid,name,allarea area,st_asgeojson(geom) as geometry from %s) tb; ' % tbname
    return sql

def impDat(tbname,gid):
    sql = 'select row_to_json(tb) as json from (select id,bkuid,mapid,levelid,type typeid,name,allarea area,st_asgeojson(geom) as geometry from %s where id > %s order by id) tb; ' % (tbname,gid)
    print(sql)
    dts=pgcnn.query(sql).namedresult()
    c = 0
    d = 0
    _start = datetime.now()
    tms = 0
    for dt in dts:
        dt.json['device_table']='public.water_layer'
        geo = dt.json['geometry']
        if geo:
            dt.json['geometry']=json.loads(geo)
            if dt.json['geometry']["type"] == 'MultiPolygon':
                dt.json['geometry']["type"] = 'Polygon'
                dt.json['geometry']["coordinates"] = dt.json['geometry']["coordinates"][0]
        #    break
        dt.json['provice']='grid'
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
    print 'insert time: %s'% tms


#tbrows = ['jilin_landuse_layer','jilin_place_label_layer','jilin_road_layer','jilin_water_layer']
log = open('./errorIds_water.log','a')
tbrows = ['water']
for tbname in tbrows:
    print(tbname)

    gid = '58971831'
	
    log.write('\ntb:%s\n'%(tbname))
    while True:
        try:
            impDat(tbname,gid)
            break
        except pymongo.errors.WriteError  as e:
            p = e.message.find('id:')
            if p > 0:
                eid = e.message[p:p+17]
                print 'WriteError:',eid
                gid = eid.split(':')[1]
                log.write(gid + ',')
                continue
            else:
                print e
                break
        break

    
    

    

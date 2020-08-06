# 注意mongodb循环插入数据的话，程序的数据对象会被注入本次插入数据的'_id'
# 循环插入需要移除或显式指定'_id'
import json
import pymongo
from pg import DB
from datetime import datetime

from dbconfig import *
pgcnn = DB(dbname=pgName,host=pgHost,port=pgPort,user=pgUser,passwd=pgPswd)
mgcnn = pymongo.MongoClient(mgHost,mgPort)
cndata = mgcnn[mgDatabase][mgCollection]

#_start = datetime.now()
#print 'remove layer ...'
#cndata.remove({'device_table':'public.landuse_layer'})
#_end = datetime.now()
#tm = _end - _start
#print 'layer removed time: %ss'% tm.seconds

def impData(tbname,gid):
    sql = '''select row_to_json(tb) as json from 
        (select id,bkuid,mapid,levelid,type typeid,name,allarea area,
        st_asgeojson(geom) as geometry from %s 
        where id > %s order by id) tb; ''' % (tbname,gid)
    #print(sql)
    items = pgcnn.query(sql).namedresult()
    c = 0
    d = 0
    _start = datetime.now()
    tms = 0
    for item in items:
        item.json['device_table']='public.landuse_layer'
        item.json['typeid'] = 40
        geo = dt.json['geometry']
        if geo:
            item.json['geometry']=json.loads(geo)
            if item.json['geometry']["type"] == 'MultiPolygon':
                num = 1
                for cds in item.json['geometry']["coordinates"]:
                    item.json['geometry']["type"] = 'Polygon'
                    item.json['geometry']["coordinates"] = cds
                    if num > 1:
                        del item.json['_id']
                        print '\nMultiPolygon id=%s,num=%s' % (item.json['id'],num)
                    _s = datetime.now()
                    cndata.insert(dt.json)
                    _e = datetime.now()
                    tm = _e - _s
                    tms = tms + tm.microseconds
                    num = num + 1
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
log = open('./building.log','a')

for tbname in ['water']:
    print(tbname)
    gid = '1'
    log.write('\ntb:%s\n'%(tbname))
    while True:
        try:
            impData(tbname,gid)
        except pymongo.errors.WriteError  as e:
            p = e.message.find(' id:')
            if p > 0:
                eid = e.message[p+2:p+18]
                gid = eid.split('')[1].strip(',')
                log.write('Error on id ='gid + '\n')
                log.write(e.message)
                print 'Error id = ',gid
                continue
            else:
                print e.message
                break
        break

    
    

    

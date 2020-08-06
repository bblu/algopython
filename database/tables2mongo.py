import re
import json
import pymongo
from pg import DB
from datetime import datetime

pgcnn=DB(dbname='dbname',host='19.16.1.2',port=5432,user='postgres',passwd='pswd')

mgcnn=pymongo.MongoClient('192.168.1.2',27017)
_start = datetime.now()
cndata=mgcnn['zoomway-db-internal'].data_tx

def genSql(tbname):
    global pgcnn,edgeid
    subsql = ''
    if tbname.startswith('roadsegment_'):
        subsql = '''select roadid as osm_id,roadname as name,routeno,mapid,
            st_asgeojson(st_linemerge(geom)) as geometry,
            linktype,length,roadclass,showgrade levelid,
            case 	when iftunnel = 1 then 'tunnel'
                when ifbridge = 1 then 'bridge'
		when ifsink	  = 1 then 'ford'
		when ifoverhead = 1 then 'overhead'
            end
            as structure 
            from %s where showgrade <= 5'''%tbname
    else:
        psql = "select column_name,data_type from information_schema.columns where table_schema='dwzy_jm' and table_name = '%s'" % tbname
        columns = pgcnn.query(psql).namedresult()
        subsql='select '
        exName=''
        for tup in columns:
            name = tup.column_name
            if name == 'oid':
                name = name + ' as zw_fid'
            elif name == 'shape' or name == 'geom':
                name = 'st_asgeojson(%s) as geometry' % name
            elif name == 'sbmc':
                name = name + ',%s as zw_name'%name
            elif name == 'type':
                name = name + ',%s as zw_type, %s as zw_subtype' % (name,name)
            elif name == 'ssds':
                exName = 'ssds'
            elif name == '_checksum' and name =='':
                exName = '_checksum'
            subsql+=name+','

        if subsql.find('zw_name')<0 and (exName == 'ssds' or exName=='_checksum'):
            subsql += '%s as zw_name,'%exName

        if subsql.find('zw_type')<0 and (exName == 'ssds' or exName=='_checksum'):
            subsql += '%s as zw_type, %s as zw_subtype,'%(exName,exName)

        if subsql.find('zw_name')<0:
            print 'error:zw_name '+tbname
        if subsql.find('zw_type')<0:
            print 'error:zw_type '+tbname
            
        subsql = subsql.rstrip(',')
        subsql += ' from dwzy_jm.%s'% tbname
    #print 'subsql:',subsql
    sql ='select row_to_json(tb) as json from (%s) tb' % subsql    
    return sql

def impData(sql,devName):
    global pgcnn
    dts=pgcnn.query(sql).namedresult()
    #print dts.count;
    #return
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
pgtbs=pgcnn.query("select tablename from pg_tables where schemaname='dwzy_jm' and tablename like 't_tx_%' order by tablename;")
tbrows=pgtbs.namedresult()
#tbrows = ['jilin_landuse_layer','jilin_place_label_layer','jilin_road_layer','jilin_water_layer']

log = open('./errorIds.log','a')
for tbrow in tbrows:
    tbname = tbrow.tablename
    if tbname.endswith('_ver'):
        continue
    devname = tbname
    #print 'remove %s from mongo ...'% devname
    #cndata.remove({'device_table':'public.%s'%devname})
    _end = datetime.now()
    tm = _end - _start
    #print '%s removed time: %ss'% (tbname,tm.seconds)
    
    #print tbname,devname
    log.write('\ntb:%s,dev:%s\n'%(tbname,devname))

    while True:
        sql = genSql(tbname)
        #print(sql)
        try:
            impData(sql,devname)
            break
        except pymongo.errors.WriteError  as e:
            p = e.message.find('oid:')
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
    

    

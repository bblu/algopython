# -*- coding: utf-8 -*-
'''
dtm2mongo 处理的数据包含
道路：roadsegment[1—14]的范围是（1,2,3...13）
铁路：railway
绿地：green
水面：water
标注：text
兴趣点：poi
建筑物：building
'''

import json
import pymongo
from datetime import datetime
from dbaUtil import pgUtil


Max4once = 500000


class DTM2Mongodb:
    def __init__(self, pg, mg):
        self.pg = pg
        self.mg = mg

    def all2mongodb(self):
        self.road2mongodb()
        self.watergreen2mongodb()

    def road2mongodb(self):
        print '|-*-start roadsegment to mongodb wait ...'

        for i in range(12, 14):
            table = 'roadsegment_%s' % i
            start = datetime.now()
            self.road2mongodb_imp(table)
            span = datetime.now() - start
            print '    |-import %s to mongodb time = %ss' % (table, span.seconds)

    def sql4road(self, table, schema='public'):
        sql = '''select roadid as id, roadname as name, routeno, mapid,roadclass,
        st_asgeojson(st_linemerge(geom)) as geometry,linktype,length,showgrade levelid
        case when iftunnel  = 1 then 'tunnel'
             when ifbridge  = 1 then 'bridge'
             when ifsink    = 1 then 'ford'
             when ifoverhead= 1 then 'overhead'
        end as structure from %s where showgrade <=5''' % (schema, table)
        return 'select row_to_json(tb) from (%s) tb' % sql

    def road2mongodb_imp(self, table):
        cnt = self.pg.count(table)
        print '    |-import %s to mongodb for %s items ...' % (table, cnt)
        sql = self.sql4road(table)
        res = self.pg.query(sql).namedresult()
        col, index = 0, 0
        for row in res:
            row.json['device_table'] = 'public.road_layer'
            geostring = row.json['geometry']
            if geostring:
                row.json['geometry'] = json.loads(geostring)
            self.mg.insert(row.json)
            col, index = col+1, row+1
            if col == 10000:
                print index
                col = 0
            elif col % 2000 == 0:
                print index,
        print index

    def railway2mongodb(self, table='railway'):
        sql = '''select id, mapid, name, levelid, type typeid, allarea area, st_asgeojson(geo) geometry,
        from %s.%s order by id''' % (self.pg.schema, table)
        res = self.pg.getjsonbyinnersql(sql)
        for row in res:
            row.json['device_table'] = 'public.%s_layer' % table
            string = row.json['geometry']
            geo = json.loads(string)
            if geo['type'] == 'MultiPolygon':
                geo['type'] = 'Polygon'
                geo['coordinates'] = geo['coordinates'][0]
            row.json['geometry'] = geo
            self.mg.insert(row.json)

    # update green set allarea=r.allarea from
    # (select bkuid,sum(area) allarea from public.green group by bkuid) as r
    # where r.bkuid = green.bkuid
    # - watergreen2mongodb --------------------------------------------- #
    def watergreen2mongodb(self):
        log = open('./error_id_water_green.log', a)
        gid = '0'
        for table in ['water', 'green']:
            while True:
                try:
                    self.water2mongodb_imp(table, gid)
                except pymongo.errors.WriteError as e:
                    p = e.message.find(', id:')
                    if p > 0:
                        gid = e.message[p+2: p+18].split()[1].rstrip(',')
                        log.write('error id:%s' % gid)
                        print 'error id:%s' % gid
                    else:
                        print e.message
                        break

    def watergreen2mongodb_imp(self, table, gid):
        sql = '''select id, mapid, name, levelid, type typeid, allarea area, st_asgeojson(geo) geometry,
        from %s where id > %s order by id''' % (table, gid)

        res = self.pg.getjsonbyinnersql(sql)
        for row in res:
            row.json['device_table'] = 'public.%s_layer' % table
            string = row.json['geometry']
            geo = json.loads(string)
            if geo['type'] == 'MultiPolygon':
                geo['type'] = 'Polygon'
                geo['coordinates'] = geo['coordinates'][0]
            row.json['geometry'] = geo
            self.mg.insert(row.json)


if __name__ == '__main__':
    pg = pgUtil('127.0.0.1', 5432, 'china', 'postgres', '123456', 'public')
    dtm2Mongo = DTM2Mongodb(pg)

    #全部导入
    dtm2Mongo.all2mongodb()
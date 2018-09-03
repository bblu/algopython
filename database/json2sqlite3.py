import json
import sqlite3

sqlite = sqlite3.connect('./sqlproject.db')
notInit = True

def init(item):
    sk = '_id integer primary key, coordinates text NULL'
    for key in item.keys():
        if key != '_id':
            sk += ',' + key + ' text NULL'
    print sk
    sqlite.execute("create table project (%s)" % sk)

c = 0
for line in open('./mgexport.json','r').readlines():
    item = json.loads(line)
    if notInit:
        init(item)
        notInit = False
    if 'geometry' in item.keys():
        item['coordinates'] = json.dumps(item['geometry']['coordinates'])
        del item['geometry']
        #print item.keys()
    if 'shape' in item.keys():
        del item['shape']

    fs = ''
    vs = ''
    for key in item.keys():
        fs += key +','
        vs += '?,'
    fs = fs[:-1]
    vs = vs[:-1]
    sql = 'insert into project (%s) values(%s)'%(fs,vs)
        #print sql
        #print item.values()
    sqlite.execute(sql, item.values())
    sqlite.commit()
    print item['_id']
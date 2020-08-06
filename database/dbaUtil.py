#
from pg import DB

class pgUtil:
    #__slots__=['connection','schema']

    def __init__(self, hot, pot, dbn, usr, pwd, shm='public'):
        self.db = DB(dbname=dbn, host=hot, port=pot, user=usr, passwd=pwd)
        self.schema = shm
        shape_val = '''st_asgeojson(st_transform(shape,4326)) shape,
        st_asgeojson(st_boundary(st_transform(shape,4326))) bound, '''
        self.colMap = {'oid'   : 'oid, oid zw_fid, ',
                       'sbmc'  : 'sbmc, sbmc zw_name, ',
                       'type'  : 'type, type zw_type, ',
                       'sbzlx' : 'sbzlx, sbzlx zw_subtype, ',
                       'shape' : shape_val}

    def setschema(self, shm):
        self.schema = shm

    def count(self, name):
        sql = 'select count(*) cnt from %s.%s;' % (self.schema, name)
        res = self.db.query(sql).namedresult()
        return res[0].cnt

    def setsrid(self, table, column, srid):
        sql = 'ALTER TABLE %s.%s ALTER COLUMN %s TYPE geometry USING ST_SETSRID(%s, %s);' % (self.schema, table, column, column, srid)
        self.db.query(sql)

    def getjsonbyinnersql(self,sql):
        json = 'select row_to_json(tb) as json from (%s) tb;' % sql
        return self.db.query(json)


    def column(self, name):
        sql = '''select column_name, data_type from information_schema
        where table_schema='%s' and table_name='%s';''' % (self.schema, name)
        return self.db.query(sql).namedresult()

    def sql4device(self, table, offset=0, limit=0):
        sql = 'select '
        for row in self.column(table):
            col = row.column_name
            if col in self.colMap.keys():
                sql += self.colMap[col]
            elif col == '_checksum':
                continue
            else:
                sql += col + ', '
        sql = sql.rstrip(',') + 'from %s.%s order by oid'
        if offset > 0:
            sql += 'offset %s limit %s' % (offset, limit)
        return 'select row_to_json(tb) as json from (%s) tb;' % sql

    def getdevrows(self, table, offset=0, limit=0):
        sql = self.sql4device(table, offset, limit)
        return self.db.query(sql).namedresult()

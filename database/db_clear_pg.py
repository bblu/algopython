from pg import DB

def CheckName(name):
    lst=name.split('_')
    if lst.__len__()<2:
        return False
    tail=lst[-1]
    if tail=='tst' or tail=='bak':
        return True
    if tail[-3:].isdigit(): #sys_mapcomposition1013
        return True
    return tail.isdigit()

db=DB(dbname='gis_meta',host='localhost',port=5432,user='postgres',passwd='123456')
# 1.drop test tmp tables
q=db.query("SELECT tablename FROM  pg_tables WHERE schemaname='public' and (tablename LIKE 'mdb_%' or tablename LIKE 'sys_%')")
rows=q.namedresult()

for row in rows:
      tbname=row.tablename
      if(CheckName(tbname)):
          sql="drop table %s;" % tbname;
          db.query(sql)
          print(sql)


# 2.delete data rows where sys_schemaid!=-1
q=db.query("SELECT table_name FROM information_schema.columns where table_schema='public' and (table_name LIKE 'mdb_%' or table_name LIKE 'sys_%') and column_name='sys_schemaid'")
rows=q.namedresult()

for row in rows:
    tbname=row.table_name
    sql = 'SELECT count(*) as rows FROM %s where sys_schemaid>0' % tbname
    tmp = db.query(sql)
    obj = tmp.namedresult()
    if obj[0].rows > 0:
        sql = 'DELETE FROM %s WHERE sys_schemaid > 0' % tbname
        db.query(sql)
        print('delete %d from %s;'%(obj[0].rows,tbname))
        
db.close()

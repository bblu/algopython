import os
from pg import DB

db=DB(dbname='db_meta',host='172.16.1.10',port=5432,user='postgres',passwd='password')
# 1.drop test tmp tables
q=db.query("SELECT sys_tablename AS tablename  FROM sys_component where sys_tablename like 't\_%' order by sys_tablename;")

rows=q.namedresult()
i=0
for row in rows:
    tbname=row.tablename
    cmd='pg_dump -h 172.16.1.10 -U postgres -F p -n public -s -t %s dbName >> D:/pgdata/db_meta_struct.sql' % tbname;
    os.system(cmd)
    i=i+1
    print('export table: %s ,%d' % (tbname,i))

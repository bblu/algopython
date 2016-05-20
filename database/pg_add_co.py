from pg import DB
     
db=DB(dbname='gis',host='localhost',port=5432,user='postgres',passwd='pswd')
# 1.drop tables begin with 't_'
q=db.query("SELECT tablename FROM  pg_tables WHERE schemaname='public' and tablename LIKE 't\_%'")
rows=q.namedresult()
c=0;
for row in rows:
        tbname=row.tablename
        alt='ALTER TABLE %s ADD COLUMN' % tbname
        sql='%s edittype_update_ integer' % alt
        sql='%s; %s edittime_update_ timestamp with time zone'%(sql,alt)
        sql='%s; %s editversionid_update_ bigint;'%(sql,alt)
        
        db.query(sql)
        c=c+1
        print('%d : %s' %(c,sql))
        
db.close()

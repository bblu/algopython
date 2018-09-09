
import sqlite3

sqlite = sqlite3.connect('./sqlproject.db',)
c = 1
for line in open('./test.txt','r').readlines():
    item = line[:-1].split('@')
    id = item[0]
    cd = item[1]
    sql = "update project set coordinates = '[%s]' where item_code = '%s';"%(cd,id)
    print c,sql
    c+=1
    #break
    sqlite.execute(sql)
    sqlite.commit()


import sqlite3

sqlite = sqlite3.connect('./sqlproject.db')

sql = "select * from project where item_code = '0016001200c5';"

cursor = sqlite.execute(sql)
for item in cursor:
    print item[0],item[1]
    print item[25],item[26],item[27]
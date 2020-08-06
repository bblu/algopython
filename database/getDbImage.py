#把数据库的二进制图片字段写到本地
import pymongo

cnn = pymongo.MongoClient('127.0,0,1', 27017)
coll = cnn.db.col
item = coll.find_one({'symbolId': id}, {'png': 1})
with open('%s.png' % id, 'wb') as pngfile:
    pngfile.write(item['png'])

#newFileByteArray = bytearray(newFileBytes)
#newFile.write(newFileByteArray)
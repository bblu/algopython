# -*- coding: utf-8 -*-
import io
import json
import pymongo
from bson import Binary
from BWriter import BinaryWriter

mgcnn=pymongo.MongoClient('172.17.68.69',27017)
src=mgcnn[u'zoomway_龙霄供热_internal'].data
obj = mgcnn.map.device

PACKAGE_BODY_BOOLEAN_FLAG = int('0xddffcc',16);
PACKAGE_BODY_NUMBER_FLAG = int('0xaaffcc',16);
PACKAGE_BODY_STRING_FLAG = int('0xaaffbb',16);
PACKAGE_BODY_ARRAY_FLAG = int('0xaaffdd',16);
PACKAGE_BODY_BUFFER_FLAG = int('0xccffcc',16);
PACKAGE_BODY_JSON_FLAG = int('0xbbffcc',16);
PACKAGE_BODY_NULL_FLAG = int('0xeeeeee',16);
PACKAGE_BODY_ERROR_FLAG = int('0xeeffcc',16);

stream = io.BytesIO()
bufWriter = BinaryWriter(stream)

def objectToStream(stream, obj):
    if isinstance(obj,float):
        stream.WriteInt32(PACKAGE_BODY_NUMBER_FLAG);
        stream.WriteDouble(obj)
    elif isinstance(obj,str) or isinstance(obj,unicode):
        stream.WriteInt32(PACKAGE_BODY_STRING_FLAG);
        c = stream.WriteUsrString(obj)
        #print 'write %s for %s chars' % (obj,c)
    elif isinstance(obj,list):
        stream.WriteInt32(PACKAGE_BODY_ARRAY_FLAG);
        stream.WriteInt32(len(obj))
        for o in obj:
            objectToStream(stream, o)
    elif isinstance(obj,dict):
        #0xbbffcc
        stream.WriteInt32(PACKAGE_BODY_JSON_FLAG)
        keys = []
        for key in obj.keys():
            keys.append(key)
        #print 'keys=%s' % keys
        stream.WriteInt32(len(keys))
        for (k,v) in obj.items():
            objectToStream(stream, k)
            objectToStream(stream, v)


def getBinary(s,obj):
    w = BinaryWriter(s)
    objectToStream(w,obj)
    return  Binary(bytes(s.getvalue()))

classDict = {
'593':'7d141d55-cca1-11e6-9d41-c5407f31c5f2',   # 弯头 3271
'595':'35474415-cca2-11e6-9d41-c5407f31c5f2',   # 变径 397
'594':'1234b075-cca2-11e6-9d41-c5407f31c5f2',   # 三通 4365
'602':'ed3dc845-cca8-11e6-9d41-c5407f31c5f2',   #补偿器 4
'588':'t_tx_hnrl_jd',                           #阀门 7903
'590':'t_tx_hnrl_fmj',                          #阀门井 1060
'597':'4e878d95-cca7-11e6-9d41-c5407f31c5f2',   #管线 16385
'596':'5e3579f5-cca2-11e6-9d41-c5407f31c5f2'}   #除污器 700

res = src.find({})
c=0
for row in res:
    #print row['_id']
    shape = row['geometry']
    row['geometry_']=shape
    stream = io.BytesIO()
    row['geometry'] = getBinary(stream,shape)
    row['@@classname'] = classDict[row['zw_type']]
    obj.insert(row)
    c+=1
    
print c


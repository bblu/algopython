#poi GB18030
import json
import pymongo
from bson import Binary
from BWriter import BinaryWriter

mgcnn=pymongo.MongoClient(mgHost,mgPort)
src = mgcnn[].data
obj = mgcnn.sggis.device

PACKAGE_BODY_BOOLEAN_FLAG = int('0xddffcc',16);
PACKAGE_BODY_NUMBER_FLAG = int('0xaaffcc',16);
PACKAGE_BODY_STRING_FLAG = int('0xaaffbb',16);
PACKAGE_BODY_ARRAY_FLAG = int('0xaaffdd',16);
PACKAGE_BODY_BUFFER_FLAG = int('0xccffcc',16);
PACKAGE_BODY_JSON_FLAG = int('0xbbffcc',16);
PACKAGE_BODY_NULL_FLAG = int('0xeeeeee',16);
PACKAGE_BODY_ERROR_FLAG = int('0xeeffcc',16);


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
        print 'keys=%s' % keys
        stream.WriteInt32(len(keys))
        for (k,v) in obj.items():
            objectToStream(stream, k)
            objectToStream(stream, v)

def getBinary(s,obj):
    w = BinaryWriter(s)
    objectToStream(w,obj)
    return  Binary(bytes(s.getvalue()))


res = src.find({})
for row in res:
    shape = row['geometry']
    row['geometry_']=shape
    stream = io.BytesIO()
    rwo['geometry'] = getBinary(stream,shape)
    row['classname'] = row['zw_type']
    obj.insert(row)
    print row['zw_fid']

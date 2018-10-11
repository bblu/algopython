# -*- coding: utf-8 -*-
import json
import pymongo


mgcnn=pymongo.MongoClient('172.17.68.69',27017)

schema = mgcnn.map.schema
data = mgcnn.map.device

def listClass():
    result=schema.find({},{'_id':1,'name':1,'alias':1})
    print result.count()
    c=1
    for obj in result:
        name = obj['alias']
        clsn = obj['name']
        
        #data.update({'_id':obj['_id']},{'$set':{'zw_subtype':'59722'}})
        print "'%s':'%s',"%(name,clsn)
        c+=1

classDict = {
'593':'7d141d55-cca1-11e6-9d41-c5407f31c5f2',   # 弯头 3271
'595':'35474415-cca2-11e6-9d41-c5407f31c5f2',   # 变径 397
'594':'1234b075-cca2-11e6-9d41-c5407f31c5f2',   # 三通 4365
'602':'ed3dc845-cca8-11e6-9d41-c5407f31c5f2',   #补偿器 4
'588':'t_tx_hnrl_jd',                           #阀门 7903
'590':'t_tx_hnrl_fmj',                          #阀门井 1060
'597':'4e878d95-cca7-11e6-9d41-c5407f31c5f2',   #管线 16385
'596':'5e3579f5-cca2-11e6-9d41-c5407f31c5f2'}   #除污器 700

for (k,v) in classDict.items():
    c = data.update({'@@classname':k},{'$set':{'@@classname':v }},multi=True)
    #result=data.find({'zw_type':k},{'_id':1})
    #print result.count()
    #c=1
    #for obj in result:
    #    data.update({'_id':obj['_id']},{'$set':{'@@classname':v }})
    #    c+=1
    print k, v, c

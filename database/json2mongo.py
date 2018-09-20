# -*- coding: utf-8 -*-
import json
import pymongo


mgcnn=pymongo.MongoClient('172.168.111.250',27017)
data=mgcnn.jilin_baishan.data
#cndata.remove({'device_table':'public.road_label_layer'})


for line in open('pipe.json','r').readlines():
    obj = json.loads(line)
    print obj['zw_fid']
    data.insert(obj)

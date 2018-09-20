# -*- coding: utf-8 -*-
import json
import pymongo
'''

投影 124.340236603852 	43.171432323841 	124.340016156371 	43.170859237750 
实测 124.341068005556 	43.171063922222 	124.340847536111 	43.170490775000
----------------------------------------------------------------------------------------
    -0.000831401704 	0.000368401619 	        -0.000831379740 	0.000368462750 
			
评-0.000831390722 	0.000368432184 		
'''
deltaLon = -0.000831390722
deltaLat =  0.000368432184

mgcnn=pymongo.MongoClient('192.168.110.21',27017)
data=mgcnn.xiamen_internal_0921.data
#result=data.find({ "zw_type": "597" })

#更新同一个对象的多个子对象只有最后一个被执行了,要合并到一个操作中！
result = data.update_many({ 'zw_type': {'$ne' : '597' }},
 {'$inc':{'geometry.coordinates.0':deltaLon,'geometry.coordinates.1':deltaLat}})

print result.modified_count

result = data.update_many({ "zw_type": "597"},
 {'$inc':{'geometry.coordinates.0.0':deltaLon,'geometry.coordinates.0.1':deltaLat,
'geometry.coordinates.1.0':deltaLon,'geometry.coordinates.1.1':deltaLat}})

print result.modified_count

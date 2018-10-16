import pymongo


mgcnn=pymongo.MongoClient('172.173.168.169',27017)
obj = mgcnn[u'zoomway_comp_internal'].data

#obj.update({"zw_jobId":"0xff7c98a2c70-dc7c-11e6-a83c-070be305ac7f"},{'$set':{"zw_jobId":"0xff76a51ca70-523c-11e7-be3a-cfadb1a9e989"}},multi=True)

u = obj.update({'zw_jobId': { '$exists': True }},{'$unset':{'zw_editStatus':''}},multi=True)

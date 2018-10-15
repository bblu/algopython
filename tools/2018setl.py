# -*- coding: utf-8 -*-
import json
import pymongo

mgcnn=pymongo.MongoClient('localhost',27017)

data=mgcnn.foo.comp
years=[]
ynums={}
ymark={}
ymax={}
ymin={}
comp={}
obj = json.load(open('2018setl.json'))
print(obj['total'])
for p in obj['rows']:
    del p['internetAnnual']
    del p['idCardSHA']
    del p['insertTime']
    del p['md5Code']
    del p['integralQualified']
    for i in range(1,11):
        del p['s%s'%i]
    p['region']=p["idCard"][0:6]
    y = int(p["idCard"][6:10])
    c = p['unit']
    if y not in years:
        years.append(y)
        ynums[y] = 0
        ymark[y] = 0
        ymax[y] = 0
        ymin[y] = 200
    if c not in comp.keys():
        comp[c] = 1
    else:
        comp[c] += 1
    ynums[y] += 1
    s = p['score']
    ymark[y] += s
    if s > ymax[y]:
        ymax[y] = s
    if s < ymin[y]:
        ymin[y] = s
    #print p
    #break
    #data.insert(p)
al = 0
for (k,v) in comp.items():
    data.insert({'comp':k,'nums':v})
print v
y70 = 0
y80 = 0
for (k,v) in ynums.items():
    if v > 0:
        print '%s：num:%03d，min:%s, max:%s, avg:%s，rate:%s%%'%(k,v,ymin[k],ymax[k],round(ymark[k]/v,2),round((v*100.0)/6019.0,3))

    if k > 1969 and k < 1980:
        y70 += v
    if k > 1979:
        y80 += v

print round((y70*100.0)/6019.0,3)
print round((y80*100.0)/6019.0,3)
'''
1958：num:001，min:95.37, max: 95.37, avg:95.37，rate: 0.017%
1959：num:001，min:93.88, max: 93.88, avg:93.88，rate: 0.017%
1960：num:001，min:92.34, max: 92.34, avg:92.34，rate: 0.017%
1961：num:001，min:93.96, max: 93.96, avg:93.96，rate: 0.017%
1963：num:001，min:97.46, max: 97.46, avg:97.46，rate: 0.017%
1964：num:005，min:93.08, max: 97.04, avg:94.85，rate: 0.083%
1965：num:002，min:95.42, max: 99.25, avg:97.34，rate: 0.033%
1966：num:003，min:91.34, max:103.50, avg:97.67，rate: 0.050%
1967：num:004，min:92.08, max: 99.33, avg:95.24，rate: 0.066%
1968：num:001，min:92.55, max: 92.55, avg:92.55，rate: 0.017%
1969：num:009，min:90.83, max: 97.83, avg:93.87，rate: 0.150%
1970：num:004，min:91.17, max: 94.92, avg:93.37，rate: 0.066%
1971：num:238，min:90.75, max:115.25, avg:97.07，rate: 3.954%
1972：num:378，min:90.75, max:122.59, avg:97.61，rate: 6.280%
1973：num:507，min:90.75, max:111.70, avg:96.80，rate: 8.423%
1974：num:586，min:90.75, max:121.25, avg:96.73，rate: 9.736%
1975：num:757，min:90.75, max:118.21, avg:96.32，rate:12.577%
1976：num:813，min:90.75, max:110.79, avg:95.74，rate:13.507%
1977：num:799，min:90.75, max:114.88, avg:95.58，rate:13.275%
1978：num:773，min:90.75, max:112.25, avg:94.74，rate:12.843%
1979：num:507，min:90.75, max:105.71, avg:93.98，rate: 8.423%
1980：num:302，min:90.79, max:105.21, avg:93.95，rate: 5.017%
1981：num:162，min:90.75, max:107.25, avg:93.39，rate: 2.691%
1982：num:109，min:90.79, max:102.67, avg:93.83，rate: 1.811%
1983：num:039，min:90.79, max:100.00, avg:92.74，rate: 0.648%
1984：num:013，min:90.87, max: 98.46, avg:93.49，rate: 0.216%
1985：num:003，min:91.62, max: 94.91, avg:93.76，rate: 0.050%
'''
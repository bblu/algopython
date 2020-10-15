#coding:utf-8

years=[]
ynums={}
ymark={}
ymax={}
ymin={}
comp={}

fname = '2020setl.txt'
ttnum = 6032
with open(fname, encoding='utf-8') as f: 
    lines = f.readlines()
    
    for line in lines:
        attrs = line.split()
        y = int(attrs[2][0:4])
        ym = int(attrs[2][5:])
        #y = y*100+ym
        c = attrs[3]
        s = float(attrs[4])
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
        ymark[y] += s
        if s > ymax[y]:
            ymax[y] = s
        if s < ymin[y]:
            ymin[y] = s
        
y60 = 0
y70 = 0
y80 = 0
for (k,v) in sorted(ynums.items()):
    if k <196912:
        continue
    if v > 0:
        print('%s：num:%03d，min:%s, max:%s, avg:%s，rate:%s%%'%(k,v,ymin[k],ymax[k],round(ymark[k]/v,2),round((v*100.0)/ttnum,3)))

    if k< 1970:
        y60 += v
    elif k > 1969 and k < 1980:
        y70 += v
    elif k > 1979:
        y80 += v
print('60s=%s%%'%round((y60*100.0)/ttnum,3))
print('70s=%s%%'%round((y70*100.0)/ttnum,3))
print('80s=%s%%'%round((y80*100.0)/ttnum,3))
#print('els=%s%%'%round(((ttnum-y80-y70-y60)*100.0)/ttnum,3))

comp = sorted(comp.items(), key=lambda kv:(kv[1], kv[0]),reverse=True)
for (k,v) in comp:
    if v > 5:
        print('%s:%s'%(k,v))


'''
1961：num:002，min:98.59, max:114.91, avg:106.75，rate: 0.033%
1962：num:003，min:97.21, max:100.08, avg: 98.17，rate: 0.050%
1963：num:005，min:97.37, max:108.16, avg:102.78，rate: 0.083%
1964：num:006，min:97.58, max:104.05, avg:100.48，rate: 0.099%
1965：num:008，min:97.29, max:114.96, avg:102.22，rate: 0.133%
1966：num:009，min:97.29, max: 99.29, avg: 98.36，rate: 0.149%
1967：num:010，min:97.34, max:111.37, avg:100.37，rate: 0.166%
1968：num:006，min:97.50, max:110.41, avg:100.74，rate: 0.099%
1969：num:027，min:97.13, max:105.50, avg:100.12，rate: 0.448%
1970：num:085，min:97.16, max:111.87, avg:101.26，rate: 1.409%
1971：num:107，min:97.21, max:114.29, avg:101.70，rate: 1.774%
1972：num:108，min:97.13, max:114.46, avg:100.99，rate: 1.790%
1973：num:329，min:97.13, max:115.25, avg:101.00，rate: 5.454%
1974：num:365，min:97.13, max:124.17, avg:101.35，rate: 6.051%
1975：num:507，min:97.13, max:120.62, avg:100.92，rate: 8.405%
1976：num:636，min:97.13, max:114.13, avg:100.66，rate:10.544%
1977：num:751，min:97.13, max:119.16, avg:100.49，rate:12.450%
1978：num:808，min:97.13, max:118.37, avg:100.10，rate:13.395%
1979：num:741，min:97.13, max:110.00, avg: 99.60，rate:12.284%
1980：num:644，min:97.13, max:112.38, avg: 99.32，rate:10.676%
1981：num:468，min:97.13, max:106.08, avg: 99.05，rate: 7.759%
1982：num:290，min:97.13, max:118.21, avg: 98.93，rate: 4.808%
1983：num:083，min:97.17, max:106.00, avg: 98.86，rate: 1.376%
1984：num:030，min:97.13, max:101.55, avg: 98.40，rate: 0.497%
1985：num:003，min:97.50, max: 98.33, avg: 97.86，rate: 0.050%
1988：num:001，min:97.71, max: 97.71, avg: 97.71，rate: 0.017%

60s =  1.260%
70s = 73.558%
80s = 25.182%

北京华为数字技术有限公司:112
华为技术有限公司北京研究所:28
北京外企人力资源服务有限公司:28
腾讯科技（北京）有限公司:24
联想（北京）有限公司:24
中国新华航空集团有限公司:23
中国国际技术智力合作集团有限公司:22
新华三技术有限公司北京研究所:19
北京前锦众程人力资源有限公司:18
阿里巴巴（北京）软件服务有限公司:16
百度在线网络技术（北京）有限公司:16
用友网络科技股份有限公司:13
清华大学:12
国际商业机器（中国）投资有限公司:12
威睿信息技术（中国）有限公司:11
同方知网（北京）技术有限公司:10
中国石油天然气勘探开发研究院:10
爱立信（中国）通信有限公司:9
北京易才人力资源顾问有限公司:9
中铁电气化局集团第一工程有限公司:9
西门子（中国）有限公司:8
联想（北京）信息技术有限公司:8
神州数码（中国）有限公司:8
甲骨文（中国）软件系统有限公司:8
戴尔(中国)有限公司北京分公司:8
同方威视技术股份有限公司:8
北京小米移动软件有限公司:8
北京嘀嘀无限科技发展有限公司:8
北京南天软件有限公司:8
阿里巴巴科技（北京）有限公司:6
英特尔（中国）有限公司北京分公司:6
联想移动通信科技（北京）有限公司:6
国际商业机器（中国）有限公司北京分公司:6
华夏银行股份有限公司:6
北京奇艺世纪科技有限公司:6
北京京东世纪贸易有限公司:6
中铁十四局集团房桥有限公司:6
中科软科技股份有限公司:6
'''

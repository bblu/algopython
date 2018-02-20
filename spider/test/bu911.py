#!/usr/bin/env python
# -*-coding:utf-8-*-
import  urllib2
from pg import DB
from lxml import etree
import os

header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)"
            #, "Connection": "keep-alive"
         }

"""
something you know

"""
curDir = 'movielist1'

def  spdDownlist():
    req = urllib2.Request("https://www.susu.com/htm/index.htm",headers=header)
    html = urllib2.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)

    #首先获取页码数,然后用循环的方式挨个解析每一个页面
    #pages = htmlpath.xpath('//div[@class="mainArea1 px9"]/ul/a/@href')
    #for page in pages:
    #    print page

    for i in range(1,8):
        print '>downlist%s:'%i,
        curDir = 'downlist%s'%i
        if not os.path.exists(curDir):
            os.mkdir(curDir)
        pageIndex = "https://www.susu.com/htm/movielist%s/" % i
        spdPages(pageIndex)
        
def  spdMovielist():
    req = urllib2.Request("https://www.susu.com/htm/index.htm",headers=header)
    html = urllib2.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)

    #pages = htmlpath.xpath('//div[@class="mainArea1 px9"]/ul/a/@href')
    #for page in pages:
    #    print page

    for i in range(1,5):
        print '>movielist%s:'% i,
        curDir = 'movielist%s'%i
        if not os.path.exists(curDir):
            os.mkdir(curDir)
        pageIndex = "https://www.susu.com/htm/movielist%s/" % i
        spdPages(pageIndex)
        #break

def spdPages(url):
    #global fil0
    try:
        req = urllib2.Request(url, headers=header)
        html = urllib2.urlopen(req)
        htmldata = html.read()
        htmlpath = etree.HTML(htmldata)

        tailPg = htmlpath.xpath('//div[@class="pageList"]/a/@href')[-1]
        print '1 -->',tailPg[0:2]
        pgNum = int(tailPg[0:2])+1
        for i in range(1,pgNum):
            page = url + '%s.htm' % i
            print page
            getPage(page)
            #break
    except Exception as e:
        print 'spdPages:',e
    

def getPage(pageUrl):
    #global fil0
    try:
        req = urllib2.Request(pageUrl, headers=header)
        html = urllib2.urlopen(req)
        htmldata = html.read()
        htmlpath = etree.HTML(htmldata)
        
        items = htmlpath.xpath('//ul[@class="movieList"]/li/a/@href')
        i=1
        for item in items:
            itemurl = "https://www.susu.com/" + item
            #print 'itemurl =',itemurl
            try:
                getPagePicturess(i,itemurl)
            except Exception:
                print 'continue'
                continue
            i=i+1
    except Exception,e:
        print '* error -- getPage:%s' % e

db=DB(dbname='postgres',host='localhost',port=5432,user='postgres',passwd='123456')
#log = open('./error.log','w')
#log = codecs.open('./error.log','w')
def getPagePicturess(i,albumsurl):
    global db,log,curDir
    req = urllib2.Request(albumsurl, headers=header)
    html = urllib2.urlopen(req)
    htmldata = html.read()
    #fil0.write(htmldata)
    htmlpath = etree.HTML(htmldata)
    infoList = htmlpath.xpath('//ul[@class="movieInfoList"]/li/text()')
    title = infoList[0]
    time = infoList[1]
    klass = htmlpath.xpath('//ul[@class="movieInfoList"]/li/a/strong/text()')[0]
    imgurl = htmlpath.xpath('//div[@class="poster"]/img/@src')[0]

    #mp4url = htmlpath.xpath('//input[@name="CopyAddr1"]/@value')
    mp4url = htmlpath.xpath('//div[@class="ndownlist"]/script[2]/text()')[0]
    mp4url = 'http://m.123456xia.com:888' + mp4url.split('"')[1]
    
    #print imgurl
    #print mp4url
    vname = os.path.basename(mp4url)
    iname = title + '-' + os.path.basename(imgurl)
    sql = "insert into bu911(type,title,imgname,vdoname,imgurl,vdourl,uptime,bimg)"
    sql = "%s values('%s','%s','%s','%s','%s','%s', to_timestamp('%s','YYYY-MM-DD HH24:MI:SS'),true)"%(sql,klass,title,iname,vname,imgurl,mp4url,time)
    #print sql
    try:
        db.query(sql)
    except Exception,e:
        print 'picture:%s'% e
        #print sql
        err = "insert into wrong(errstr,url) values('%s','%s')"%(e,albumsurl)
        db.query(err)
    filePath = '%s/%s' % (curDir, iname )
    if os.path.isfile(filePath):
        print i,filePath
    else:
        print '%s:%s,%s,%s'%(i,klass,title,time)
        savePicture(iname,filePath,imgurl)

def savePicture(fileName,filePath,imgurl):
    global db
    
    #print fileName
    try:
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)"
                #, "Connection": "keep-alive"
        }
        req = urllib2.Request(imgurl, headers=headers)

        urlhtml = urllib2.urlopen(req)
        respHtml = urlhtml.read()
        #print 'save file:', filePath
        binfile = open(filePath , "wb")
        binfile.write(respHtml);
        binfile.close();
    except Exception,e:
        print 'save:%s=>%s'%(e,imgurl)
        err = "insert into wrong(errstr,url) values('%s','%s')"%(e,imgurl)
        db.query(err)

spdMovielist()
#spdDownlist()
"""
fl=open('list.txt', 'w')
for i in pciturelist:
    fl.write(i)
    fl.write("\n")
fl.close()
print '关机ing'
"""
#print 'finish'
#system('shutdown -s')

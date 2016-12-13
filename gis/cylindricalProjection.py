# -*- coding:utf-8 -*- 
import os,sys
import math
from PIL import Image

#51，16
#484，0
R=38.0
r=500.0

srcPic = Image.open('prjNT.jpg')
#srcPic = Image.open('centrum.jpg')
srcPixWidth,srcPixHeight=srcPic.size
print "srcPixSize = (",srcPixWidth,",",srcPixHeight,')' #280x50
srcPixHalfWidth=(srcPixWidth+1)/2.0
if (srcPixWidth % 2) == 0:
    srcPixHalfWidth=srcPixWidth/2.0
    
srcPixHalfHeight = (srcPixHeight+1)/2.0
if (srcPixHeight % 2) == 0:
    srcPixHalfHeight = srcPixHeight/2.0
print "srcPixhalfSize = (",srcPixHalfWidth,",",srcPixHalfHeight,')' #280x50
betaMax=math.asin(R/(R+r))
#print "betaMax =",betaMax,"degMax=", betaMax*180/math.pi
alphaMax=math.pi/2-betaMax
print "alphaMax =",alphaMax,"degMax=", alphaMax*180/math.pi
arcMax = alphaMax*R
print " arcMax = ",alphaMax,'*',R,'=',arcMax,'mm'

srcHalfWidth=r*math.tan(betaMax)
srcWidth = srcHalfWidth * 2
#print "srcHalfWidth=",srcHalfWidth, 'srcWidth =',srcWidth,'mm'
scalePermm = srcPixWidth/srcWidth 
print "scalePermm = ",srcPixWidth,'/',srcWidth,'=',scalePermm,"pix/mm"
pixR=R*scalePermm
pixr=r*scalePermm
print "pixR =",pixR,"pixr =",pixr
objHalfPixWidth = (int)(math.ceil(arcMax*scalePermm))
objPixWidth = objHalfPixWidth * 2+1
objPixHeight = srcPixHeight
print "objPixSize =(",objPixWidth,objPixHeight,')'
objHalfPixHeight = (objPixHeight+1)/2

last=0.0
def getPrjX(x):
    global last, pixR, pixr, srcPixHalfWidth, objHalfPixWidth
    if(x==objHalfPixWidth):
        return srcPixHalfWidth
    if(x<objHalfPixWidth):
        arc = (objHalfPixWidth-x)/pixR
        h = pixR * math.sin(arc)
        l = pixR * math.cos(arc)
        prjx = pixr*h/(pixr+l)
        beta = math.atan(prjx/pixr)
        #print w,last-prjx,srcPixHalfWidth - prjx,arc,beta
        return srcPixHalfWidth - prjx
    if(x>objHalfPixWidth):
        arc = (x-objHalfPixWidth)/pixR
        h = pixR * math.sin(arc)
        l = pixR * math.cos(arc)
        prjx = pixr*h/(pixr+l)
        beta = math.atan(prjx/pixr)
        #print w,last-prjx,srcPixHalfWidth - prjx,arc,beta
        return srcPixHalfWidth + prjx

    
def getInt(v1,v2,v3,v4,w1,w2,w3,w4):
    return int(math.floor(v1*w1+v2*w2+v3*w3+v4*w4))

def getNTPix(x,y):
    global srcPic,srcPixWidth,srcPixHeight
    w=int(round(x))
    h=int(round(y))
    if w == srcPixWidth:
        w = srcPixWidth-1
    if h == srcPixHeight:
        h = srcPixHeight-1
    return srcPic.getpixel((w,h))

def getDLPix(x,y):
    global srcPic,srcPixWidth,srcPixHeight
    if x+1 > srcPixWidth:
        x = srcPixWidth-1
    if y+1 > srcPixHeight:
        y = srcPixHeight-1
    cy=math.ceil(y)
    if cy<1:
        cy=1
    fy=cy-1
    cx=math.ceil(x)
    if cx<1:
        cx=1
    fx=cx-1
    
    #print fx,x,cx,fy,y,cy
    w1=(cx-x)*(cy-y)
    w2=(x-fx)*(cy-y)
    w3=(cx-x)*(y-fy)
    w4=(x-fx)*(y-fy)

    if ( x-math.floor(x)>1e-5 or y-math.floor(y)>1e-5 ):
        r1,g1,b1 = srcPic.getpixel((fx,fy))
        r2,g2,b2 = srcPic.getpixel((cx,fy))
        r3,g3,b3 = srcPic.getpixel((fx,cy))
        r4,g4,b4 = srcPic.getpixel((cx,cy))
        r = getInt(r1,r2,r3,r4,w1,w2,w3,w4)
        g = getInt(g1,g2,g3,r4,w1,w2,w3,w4)
        b = getInt(b1,b2,b3,r4,w1,w2,w3,w4)
        return (r,g,b)
    else:#print x,y
        return srcPic.getpixel((int(x),int(y)))

def getPrjY(fy,y):
    global srcPixHalfHeight,b
    delta = (b-fy)*(1-y/srcPixHalfHeight)
    #print delta,'=',b-fy,'*',1-y/srcPixHalfHeight
    return y + delta


#Ellipse
alphaVert = math.atan(srcPixHeight/(2*pixr))
effectR = srcPixHalfWidth
a = effectR
b = a * math.sin(alphaVert)
tranWb = 0
for w in range(int(srcPixHalfWidth)):
        prjX=getPrjX(w)
        if prjX>=0:
            tranWb=w
            break
print 'tranWb =',tranWb
out=3
if out==1:
    #b = 90
    objPic = Image.new('RGB',[srcPixWidth,srcPixHeight])
    pixels = objPic.load()
    for w in range(srcPixWidth):
        fx = w-srcPixHalfWidth
        fx2 = (fx/a) * (fx/a)
        fy = b * math.sqrt(1-fx2)
        for h in range(0, srcPixHeight):
            delta = (b-fy)*(1-h/srcPixHalfHeight)
            prjY= h + delta
            pixels[w,h]=getNTPix(w, prjY)
    objPic.save('prjVert.jpg','JPEG')

elif out==2:
    objPic = Image.new('RGB',[objPixWidth,objPixHeight])
    pixels = objPic.load()
    for w in range(objPixWidth):
        prjX=getPrjX(w)        
        if prjX>=0 and prjX<srcPixWidth:
            for h in range(0, objPixHeight):
                #print fx,fy, w,'->',prjX,h,'->',prjY,'delta',
                pixels[w,h]=getNTPix(prjX, h)
    objPic.save('prjHori.jpg','JPEG')
else:
    tranW = int(objPixWidth-tranWb*2)+1
    print tranWb,tranW,objPixWidth
    objPic = Image.new('RGB',[tranW,objPixHeight])    
    pixels = objPic.load()
    for w in range(tranWb,tranWb+tranW):
        prjX=getPrjX(w)
        if prjX>=0 and prjX<srcPixWidth:
            fx = prjX-srcPixHalfWidth
            fx2 = (fx/a) * (fx/a)
            fy = b * math.sqrt(1-fx2)
            if prjX>=0 and prjX<srcPixWidth:
                fy = b
                fx = prjX-effectR
                if fx>-a and fx < a:
                    fx2 = (fx/a) * (fx/a)
                    fy = b * math.sqrt(1-fx2)
                for h in range(0, objPixHeight):
                    delta = (b-fy)*(1-h/srcPixHalfHeight)
                    prjY= h + delta
                    pixels[w-tranWb,h]=getNTPix(prjX, prjY)
    objPic.save('prjAll.jpg','JPEG')

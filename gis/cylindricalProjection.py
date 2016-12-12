# -*- coding:utf-8 -*- 
import os,sys
import math
from PIL import Image

#51，16
#484，0
R=38.0
r=500.0

srcPic = Image.open('centrum.jpg')
srcPixWidth,srcPixHeight=srcPic.size
print "srcPixWidth =",srcPixWidth,"srcPixHeight=",srcPixHeight #280x50
srcPixHalfWidth=(srcPixWidth+1)/2

betaMax=math.asin(R/(R+r))
print "betaMax =",betaMax,"degMax=", betaMax*180/math.pi
alphaMax=math.pi/2-betaMax
print "alphaMax =",alphaMax,"degMax=", alphaMax*180/math.pi
arcMax = alphaMax*R
print " arcMax = ",alphaMax,'*',R,'=',arcMax,'mm'

srcHalfWidth=r*math.tan(betaMax)
srcWidth = srcHalfWidth * 2
print "srcHalfWidth=",srcHalfWidth, 'srcWidth =',srcWidth,'mm'
scalePermm = srcPixWidth/srcWidth 
print "scalePermm = ",srcPixWidth,'/',srcWidth,'=',scalePermm,"pix/mm"
pixR=R*scalePermm
pixr=r*scalePermm
print "pixR =",pixR,"pixr =",pixr
objHalfPixWidth = (int)(math.ceil(arcMax*scalePermm))
objPixWidth = objHalfPixWidth * 2+1
print "objPixWidth =",objPixWidth,'pix halfWidth =',objHalfPixWidth
srcHalfPixHeight = (srcPixHeight+1)/2
objPixHeight = srcPixHeight
print "objPixHeight =",objPixHeight
objHalfPixHeight = (objPixHeight+1)/2
objPic = Image.new('RGB',[objPixWidth,objPixHeight])
pixels = objPic.load()

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

#Ellipse
effectR = objHalfPixWidth-124
alphaVert = math.atan(srcPixHeight/(2*pixr))
b = effectR * math.sin(alphaVert)
a = effectR
print "Ellipse: a =",a,"b =",b


def getPrjY(fy,y):
    global srcHalfPixHeight,b
    delta = (b-fy)*(1-y/srcHalfPixHeight)
    return y + delta

if False:
    srcHalfPixHeight=50.0
    srcPixHalfWidth=50.0
    b=10.0
    a=50.0
    for w in range(1,99):
        for h in range(1,99):
            prjY=getPrjY(w,h)

    
def getInt(v1,v2,v3,v4,w1,w2,w3,w4):
    return int(math.floor(v1*w1+v2*w2+v3*w3+v4*w4))

def getDLPix(x,y):
    global srcPic
    x0=math.floor(x)
    x1=x0+1
    r0,g0,b0 = srcPic.getpixel((x0,y))
    r1,g1,b1 = srcPic.getpixel((x1,y))
    r=int(math.floor(r0*(x-x0)+r1*(x1-x0)))
    g=int(math.floor(g0*(x-x0)+g1*(x1-x0)))
    b=int(math.floor(b0*(x-x0)+b1*(x1-x0)))
    return (r,g,b)

def getDLPix2(x,y):
    global srcPic,srcPixWidth,srcPixHeight
    if x+1 > srcPixWidth:
        x = srcPixWidth-1
    if y+1 > srcPixHeight:
        y = srcPixHeight-1
    cy=math.ceil(y)
    if(cy<1):
        cy=1
    fy=cy-1
    cx=math.ceil(x)
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

for w in range(objPixWidth):
    prjX=getPrjX(w)
    fx = prjX-srcPixHalfWidth
    fx2 = (fx/a) * (fx/a)
    fy = b * math.sqrt(1-fx2)
    if(prjX>=0 and prjX<srcPixWidth):
        #print w,prjX
        for h in range(0, objPixHeight):
            prjY=getPrjY(fy,h)
            #if w==300:
#                print w,h,prjY
            pixels[w,h]=getDLPix2(prjX, prjY)

objPic.save('obj.jpg','JPEG')

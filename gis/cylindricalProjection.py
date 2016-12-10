import os,sys
import math
from PIL import Image

R=50.0
r=350.0

srcPic = Image.open('28050.bmp')
srcPixWidth,srcPixHeight=srcPic.size
print "srcPixWidth =",srcPixWidth,"srcPixHeight=",srcPixHeight #280x50

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

objHalfPixWidth = (int)(math.ceil(arcMax*scalePermm))
objPixWidth = objHalfPixWidth * 2
print "objPixWidth =",objPixWidth,'pix halfWidth =',objHalfPixWidth
objPixHeight = srcPixHeight
print "objPixHeight =",objPixHeight

objPic = Image.new('RGB',[objPixWidth,objPixHeight])
pixels = objPic.load()

for w in range(objHalfPixWidth):
    
    for h in range(0, objPixHeight):
        pix = srcPic.getpixel((w, h))
        pixels[w,h]=pix


objPic.save('obj.bmp','BMP')

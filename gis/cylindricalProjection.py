import os,sys
import math
from PIL import Image
import ImageDraw

pic = Image.open('.\\28050.bmp')

pw,ph=pic.size
print pw,ph #280x50

R=5
r=35
T=2*R*r
R=math.sqrt(T+r*r)
rw=T/R
print rw
rh=2

pw2=pw*2
ph2=ph

blank = Image.new("RGB",[pw2,ph2],"black")
#drawObject = ImageDraw.Draw(blank)
pixels = blank.load()

for w0 in range(pw/2, pw):
    
    for h0 in range(0, ph):
        pix = pic.getpixel((w, h))
        pixels[pw0,h0]=pix;

blank.

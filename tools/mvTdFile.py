import os
import sys
import shutil
#info=os.getcwd()
#listfile=os.listdir(os.getcwd())

#print(listfile)
listnames = {}
keys=[]
maxLen=0
minLen=100
movDir = 'F:/712M/'
picDir='F:/712/'
newDir = 'F:/new/'
for file in os.listdir(movDir):
    if file[0:2].isalnum():
        ls = file.split('.')
        ln = len(ls[0])
        if maxLen < ln:
            maxLen = ln
        if minLen > ln:
            minLen = ln
        listnames[ls[0]]=ls[1]
movKeys = listnames.keys()

picLst= os.listdir(picDir)
print('===[%s]-[%s]==Mcount=[%s],Pcount=[%s]'%(minLen,maxLen,len(keys),len(picLst)))

c=1
for ln in range(maxLen+1,minLen-1,-1):
    print('---[%s]'%(ln))
    for picFile in picLst:
        if picFile[0:ln] in movKeys:
            key = picFile[0:ln]
            mex = listnames[key]
            oldMovFile = movDir + key +'.'+mex
            newPicName = picFile[ln:].strip()
            newMovFile = newDir + newPicName[0:-3]+mex
            
            print(oldMovFile,'->',newMovFile)
            print(picDir+picFile,'->',newDir+newPicName)
            print(c,'-----------------------------------')
            os.rename(oldMovFile,newMovFile)
            os.rename(picDir+picFile,newDir+newPicName)
            picLst.remove(picFile)
            c = c+1

#file mytime.py
import sys,time
reps=1000
repslist=range(reps)

def timer(func, *pargs, **kargs):
    start = time.clock()
    for i in repslist:
        ret = func(*pargs,**kargs)
    elapsed = time.clock()-start
    return (elapsed, ret)

#timeeseqs.py
'''reps=1000
2.7.11+ (default, Apr 17 2016, 14:00:29) 
[GCC 5.3.1 20160413]
------------------------------
forloop  : 0.15103 => [0...999]
------------------------------
listComp : 0.09665 => [0...999]
------------------------------
mapCall  : 0.06413 => [0...999]
------------------------------
genExpr  : 0.12180 => [0...999]
------------------------------
genFunc  : 0.12264 => [0...999]

reps=10000
------------------------------
forloop  : 14.51475 => [0...9999]
------------------------------
listComp : 9.02454 => [0...9999]
------------------------------
mapCall  : 5.69827 => [0...9999]
------------------------------
genExpr  : 11.52826 => [0...9999]
'''
def forloop():
    res=[]
    for x in repslist:
        res.append(abs(x))
    return res

def listComp():
    return [abs(x) for x in repslist]

def mapCall():
    return map(abs,repslist)

def genExpr():
    return list(abs(x) for x in repslist)

def genFunc():
    def gen():
        for x in repslist:
            yield abs(x)
    return list(gen())

if __name__ == '__main__':
    print(sys.version)
    for test in (forloop, listComp, mapCall, genExpr, genFunc):
        ela,res=timer(test)
        print('-'*30)
        print('%-9s: %.5f => [%s...%s]'%(test.__name__,ela,res[0],res[-1]))
    

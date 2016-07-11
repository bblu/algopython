import random
workers = range(10)
c=3; t=1
random.shuffle(workers)
for w in workers:
    print('p[%s]\t->\tT%d'%(w,t))
    t+=1
    if(t == c+1):
        t=1

    

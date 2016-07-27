#for else by bblu @ 2016-07-21

l = [1,2,3,4,5,6,7]

def has8(lst):
    for i in l:
        if i==8:
            return True
    else:
        return False

def has(lst,num):
    for i in l:
        if i==num:
            return True
    else:
        return False

print('has8 = %s'%has8(l))
print('list.append(8)')
l.append(8)
print('has8 = %s'%has8(l))
l.append(8)
print('list.append(8)')

f = filter(lambda x:x==8,l)
print 'filter(x==8) = %s'%f

f = filter(lambda x:x<4,l)
print 'filter(x<4) = %s'%f

print len(filter(lambda x:x==9,l))==0

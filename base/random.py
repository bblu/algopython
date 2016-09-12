import random as rdm

print rdm.random()

for i in range(3):
    r = rdm.random()
    print('Random[%d]%%d = %d'%(i,r))
    print('Random[%d]%%f = %f'%(i,r))
    print('Random[%d]%%s = %s'%(i,r))

#0.321742092357
#Random[0]%d = 0
#Random[0]%f = 0.948852
#Random[0]%s = 0.948851943313
#Random[1]%d = 0
#Random[1]%f = 0.051139
#Random[1]%s = 0.0511387935717
#Random[2]%d = 0
#Random[2]%f = 0.177592
#Random[2]%s = 0.177592050423

lst=[1,2,3,4,5,6]
#avoiding a \n by what printed out is use what charactor?
print 'change lst in for didnot update the range value'
for i in range(len(lst)):
    t = rdm.choice(lst)
    lst.remove(t)
    print '%d\n'%t
print 'change lst will affect the for times'
lst=[1,2,3,4,5,6]
for i in lst:
    t = rdm.choice(lst)
    lst.remove(t)
    print t

#ch6 mylist.py
class Mylist:
    def __init__(self,lst=None):
        self.list=lst

    def __add__(self,lst):
        return self.list +lst
        
    def __item__(self,idx):
        return self.list[idx]

    def append(self,lst):
        self.append(lst)

    def sort(self):
        self.list.sort()

    def __str__(self):
        return str(self.list)
    
l1=[1,2,3]
l2=[5,4,0]

m = Mylist(l1)
m = m+l2
print(m)
print(m[1])
m.sort()
print(m)
for i in m:
    print(i)

print('-'*30)

class MylistSub(Mylist):
    def __init__(self,lst=None):
        MylistSub.numCall=0
        self.list=lst
        
    def __add__(self,lst):
        MylistSub.incCall(self)
        return Mylist.__add__(self,lst)

    def sort(self):
        MylistSub.incCall(self)
        self.list.sort()

    def incCall(self):
        MylistSub.numCall +=1
        print('numCall = %d'%MylistSub.numCall)

s=MylistSub(l2)
s.sort()
print(s)
s=s+l1
s=s+[5,7]
s.sort()
print(s)


#ch6 test

class Adder:
    def __init__(self,obj=None):
        self.obj = obj
        
    def add(self,x,y):
        print('Not Implemented')

    def __str__(self):
        return str(self.obj)

class ListAdder(Adder):
    def __add__(self,ano):
        self.obj += ano
        return self
    
    def add(self,x,y):
        return x+y;

    
class DictAdder(Adder):
    def __add__(self,ano):
        self.obj.update(ano)
        return self
    
    def add(self,x,y):
        x.update(y);
        return x

#test add
a1=Adder()
a1.add(1,2)

l1=[1,2]
l2=[3]
a2=ListAdder()
l=a2.add(l1,l2)
print(l)

d1={1:'a',3:'x'}
d2={2:'b'}
a3=DictAdder()
d=a3.add(d1,d2)
print(d)
#test +
print('+'*30)
a1 = ListAdder(l1)
a2 = a1+l2
print(a2)
a3 = DictAdder(d1)
d = a3 + d2
print(d)

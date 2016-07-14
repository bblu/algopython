class C1:
    def say(self):
        return 'c1'

class C2:
    def __init__(self,who):
        self.name=who

    def say(self):
        return 'C2'
    def __str__(self):
        return 'C2.name=%s'%self.name


#take care of the order of base class for search method in parents
class C3(C1,C2):               
    def __init__(self,who):
        self.name = who

    def setName(self, who):
        self.name = who
class C4(C3):
    def say(self):
        return 'c4 override the c1'

Ia=C3('a') 
Ib=C3('b')

Ia.setName('bob')
Ib.setName('jon')

Ic=C3('bblu')
Id=C4('doo')
l=[Ia,Ib,Ic,Id]

for i in l:
    print(i.say(), i.name)
    
Id.newname='door'

print Id.newname
print Id

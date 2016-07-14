#manager.py bu bblu @ 2016-07

class Person:
'''
create and process person records
'''
    def __init__(self, name, job=None, pay=0):
        self.name=name
        self.job=job
        self.pay=pay

    def lastName(self):
        return self.name.split()[-1]

    def giveRaise(self,percent):
        self.pay *=1+percent

    def __str__(self):
        return '[Person:%s, %s]' % (self.name, self.pay)

class Manager(Person):
    def __init__(self, name, job='mgr',pay=0):
        Person.__init__(self,name,job,pay)

    def givRaise(self,percent, bonus=.1):
        Person.giveRaise(self,percent + bonus)

    def __getattr__(self):

        return None

    def __str__(self):
        return '[Manager:%s, %s]' % (self.name, self.pay)

class Manager2:
    def __init__(self, name, pay):
        self.person = Person(name,'mgr',pay)

    def giveRaise(self,percent, bonus=.1):
        self.person.giveRaise(percent+bonus)

    
    def __getattr__(self,attr):

        return getattr(self.person, attr)

    def __str__(self):
        return '[Manager:%s, %s]' % (self.person.name, self.person.pay)

class Department:
    def __init__(self,*args):
        self.members = list(args)

    def addMember(self,person):
        self.members.append(person)

    def giveRaise(self,percent):
        for p in self.members:
            p.giveRaise(percent)

    def showAll(self):
        for p in self.members:
            print(p)
            

if __name__ == '__main__':
    bob = Person('Bob Smith')
    sue = Person('Sue Jones', job='dev', pay=1000)
    print(bob)
    print(sue)

    print(bob.lastName(),sue.lastName())
    sue.giveRaise(.20)
    print(sue)

    mgr = Manager('bos Strong','mgr',2000)
    mgr.giveRaise(.2)
    print(mgr)

    tom = Manager('tom swiss',pay=5000)
    print(tom)
    print('-'*30)
    dep = Department(bob,sue)
    dep.addMember(tom)
    dep.giveRaise(.1)
    dep.showAll()
    

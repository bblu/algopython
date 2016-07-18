#decorator tracer
class tracer:
    def __init__(self,func):
        self.calls = 0
        self.func = func

    def __call__(self, *args):
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        self.func(*args)

@tracer
def spam(a,b,c):
    print(a,b,c)

spam(1,2,3)
spam('a','b','c')
spam(4,5,6)

print('-'*30)

class Spam:
    numInstance = 0

    def __init__(self):
        Spam.numInstance +=1

    @tracer
    def printNum():
        print('Number of instances create:',Spam.numInstance)

a=Spam()
a.printNum()
b=Spam()        
      
Spam.printNum()
c=Spam()  
b.printNum()

def count(klass):
    klass.numInstances = 0
    return klass

@count
class Widget:
    def __init__(self,a):
        self.w = a

    def printw(self):
        print('self.w = ',self.w)

    def printI(self):
        print('self.numInstances = ',self.numInstances)
        
w = Widget('a')
w.printw()
w.printI()
    

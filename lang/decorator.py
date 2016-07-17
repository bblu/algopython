#decorator tracer
class tracer:
    def __init__(self,func):
        self.calls = 0
        self.func = func

    def __call__(self, *args):
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        self.func(*args)

class Spam:
    numInstance = 0

    def __init__(self):
        Spam.numInstance +=1

    @tracer
    def printNum():
        print('Number of instances create:',Spam.numInstance)


a=Spam()        
b=Spam()        
      
Spam.printNum()
c=Spam()  
a.printNum()



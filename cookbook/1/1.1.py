#python 3.4
##1.1.2
p = (1,2)
x,y = p
print('1.1 get x from array x = %d' % x)
print('1.1 get x from array y = %d' % y)


data = [ 'BBLU', 34, 50, (1982,12,15) ]
name, age, price, date = data
print(name)
print(date)

s='BBLU'
b,b,l,u = s
print(l)

##1.2
first, *middle, last = data
print(middle)

name,*_,(year,*_) = data
print('1.2 get year in data item year = %d' % year)

s1 = sum((1,2,3,4))
s1 = sum([1,2,3,4])
print('what is the different between s1 and s2?')


def avg(marks):
    sum=0
    for m in marks:
        sum+=m
    print('len=%d' % len(marks))
    return sum/len(marks)

def drop_first_last(grades):
    _, *mid, _ = grades
    print(mid)
    return avg(mid)
grades = [50,60,70,80,90]

v = drop_first_last(grades)
print(v)

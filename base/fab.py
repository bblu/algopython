#1 2 3 4 5 6
#1 1 2 3 5 8
def fab(n):
    f=1
    if n < 3:
        return f
    f=fab(n-1)+fab(n-2);
    return f
if __name__ == '__main__':
    for i in range(1,10):
        print('fab(%d)=%d'%(i,fab(i)))


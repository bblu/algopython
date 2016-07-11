#round string

def rstr(i,string):
    return string[i:]+string[0:i]

str='abcdefg'

ret = rstr(3,str)
print(ret)

# python 3 @ 8-16 in xiamen
# Chapter 1: Building Abstractions with Functions
# The fundamental equation of computers is: computer = powerful + stupid

from urllib.request import urlopen
shakespeare = urlopen('http://inst.eecs.berkeley.edu/~cs61a/fa11/shakespeare.txt')
# without network an error raised:
# urllib.error.URLError: <urlopen error [Errno -2] Name or service not known>

words = set(shakespeare.read().decode().split())
# associates the name words to the set of all unique words
# that appear in Shakespeare's plays, all 33,721 of them. 

{w for w in words if len(w) == 6 and w[::-1] in words}
# {'redder', 'drawer', 'reward', 'diaper', 'repaid'}
# The cryptic notation w[::-1] enumerates each letter in a word,
# but the -1 dictates to step backwards. 

# pure function without side effects over against unpure function
def square(x):
    return mul(x,x)



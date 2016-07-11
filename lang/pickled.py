import pickle
d={'a':1,'b':2,'c':3}
f=open('/home/bblu/repo/algopython/lang/dat.pkl','wb')
pickle.dump(d,f)
f.close()

e=open('/home/bblu/repo/algopython/lang/dat.pkl','rb')
anotherd=pickle.load(e)
print(anotherd)


c=open('/home/bblu/repo/algopython/lang/dat.pkl','rb').read()
print(c)

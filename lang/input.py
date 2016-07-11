#while input test by bblu @ 2016
while True:
    reply = input('Enter text or number:')
    if reply == 'stop': break
    try:
        num = int(reply)
    except:
        print('Bad! '*3)
    else:print(int(reply)**2)
print('Bye')

for i in [1,2,3,4,5]:
    if i==3:
        print(i)
        yield
        

#test

d = {'key1': 1, 'key2': 2, 'key3': 3, 'key4': 4, 'key5': 5}
d1 = dict(list(d.items())[len(d)//2:])
d2 = dict(list(d.items())[:len(d)//2])

#print(d1)
#print(d2)

print(dict(list(d.items())[:13]))
print(dict(list(d.items())[13:25]))
print(dict(list(d.items())[25:34]))
print(dict(list(d.items())[34:42]))
print(dict(list(d.items())[42:47]))
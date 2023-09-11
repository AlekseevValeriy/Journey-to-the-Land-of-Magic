from random import choice, choices
a = [1, 2 ,3]
b = [4, 5, 6]
v = choice(a)
a.remove(v)
print(a, v)
c = choice(a)
a.remove(c)
print(a, c)
n = choice(a)
a.remove(n)
print(a, n)

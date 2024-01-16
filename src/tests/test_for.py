a = (1, 2)
b = (2, 3)
d = (3, 4)

c = input()
print(*a if c == 'a' else b if c == 'b' else d)
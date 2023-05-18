# s = []
# width, height = int(input()), int(input())
# cat_x, cat_y = int(input()), int(input())
# scale = int(input())
# [[s.append([row, col]) for col in range(cat_x - scale, sum([cat_x, scale, 1]))] for row in range(cat_y - scale, sum([cat_y, scale, 1]))]
# matrix = [['W' if [row, col] in s else 0 for col in range(width)] for row in range(height)]
# for i in matrix:
#     print(*i, sep='\t', end='\n')
# import numpy, random
#
# a = []
# for i in range(10):
#     a.append([True] * 10)
#
# b = a[:]
# for i in enumerate(a):
#     for j in enumerate(i[1]):
#         b[i[0]][j[0]] = [j[1], i[0], j[0]]
# b = numpy.asarray(b)
# print(b)
# print(random.choice(numpy.array(b).ravel()))
#
# a = [[1, 0, 1],
#      [1, 1, 1],
#      [0, 0, 0]]
# b = []
# for y, h in enumerate(a):
#     for x, w in enumerate(h):
#         b.append((y, x)) if a[y][x] else False
#
# for line in b:
#     print(line)
# a = [[5, 3, 1], [6, 5, 1], [8, 4, 0], [8, 3, 0], [5, 6, 0], [5, 4, 0]]
# for x, y, s in a:
# #     print(x, y, s)
# import os
# # def path(file, directory=None):
# #     if directory:
# #         return os.path.join(directory, file)
# #     return os.path.join(file)
# #
# # print(path('asdd', directory='run'))
# # print(os.listdir('run'))
# # a = {'a':'b', 'c':'d'}
# #
# # def abc(b):
# #     c = {1: 2, 3: 4}
# #     for i in c:
# #         b[i] = c[i]
# # abc(a)
# # print(a)
# a = '12345'
# print(a[:2])
# class a:
#     def __init__(self):
#         self.x_position = 0
#         self.y_position = 0
#
#     def s(self):
#         key = 2
#         dba = {1: ['-x', 'left', 'goes'], 2: ['+x', 'right', 'goes'], 3: ['-y', 'up', 'goes'],
#                4: ['+y', 'down', 'goes'], False: 'worth'}
#         dba_fs = {'x': self.x_position, 'y': self.y_position, '-': lambda a, b: a - b, '+': lambda a, b: a + b}
#         if key:
#             print(dba[key][0][1])
#             dba_fs[dba[key][0][0]](dba_fs[dba[key][0][1]], 10)
#             side = dba[key][1]
#             status = dba[key][2]
#         print(self.x_position, side, status)
# b = a()
# b.s()
a = {1: [lambda a: (a * 0.5, a / 0.5), ()]}

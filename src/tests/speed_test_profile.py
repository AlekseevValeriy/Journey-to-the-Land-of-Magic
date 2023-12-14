import timeit
print(all(map(lambda o: print(o), (range(1, 100)), (range(100, 1, -1)))))
# test_dict = {'t1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0,}
# for i in range(1000):
#     test_1 = timeit.timeit("tuple(map(float, range(1000)))", number=100)
#     test_dict['t1'] += test_1
#     test_2 = timeit.timeit("tuple(map(lambda a: float(a), range(1000)))", number=100)
#     test_dict['t2'] += test_2
#     test_3 = timeit.timeit("list(map(float, range(1000)))", number=100)
#     test_dict['t3'] += test_3
#     test_4 = timeit.timeit("list(map(lambda a: float(a), range(1000)))", number=100)
#     test_dict['t4'] += test_4
#
# print(test_dict['t1'] / 1000)
# print(test_dict['t2'] / 1000)
# print(test_dict['t3'] / 1000)
# print(test_dict['t4'] / 1000)
test_dict = {'t1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0,}
for i in range(1000):
    test_1 = timeit.timeit("all(o == t for o, t in zip(range(1, 100), range(100, 1, -1)))", number=100)
    test_dict['t1'] += test_1
    test_2 = timeit.timeit("all(map(lambda o: print(o), (range(1, 100)), (range(100, 1, -1))))", number=100)
    test_dict['t2'] += test_2
print(test_dict['t1'] / 1000)
print(test_dict['t2'] / 1000)

from timeit import timeit

b = {'1': 0, '2': 0}
for _ in range(100):
    t1 = timeit("'_'.join(['down', 'run', '0'])", number=100000)
    b['1'] += t1
    t2 = timeit("""f'{"down"}_run_0'""", number=100000)
    b['2'] =+ t2
print(b)
print(b['1'] / 100)
print(b['2'] / 100)
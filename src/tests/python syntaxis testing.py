import numpy

data = numpy.array([[[1, 2, 3, 4], [-1, -2, -3, -4]], [[5, 6, 7, 8], [-5, -6, -7, -8]]])


def func(data):
    if data % 2:
        return 1
    return 0


arr = numpy.vectorize(func)(data)
print(arr)

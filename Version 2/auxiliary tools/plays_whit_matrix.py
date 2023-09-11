import math
import numpy

class Rotator:
    def __init__(self, matrix, a):
        self.matrix = matrix
        self.clear_matrix = []
        self.a = a
        self.centre_all = [[], []]
        self.centre_x = 0
        self.centre_y = 0
        self.coordinate = []

    def create_clear_matrix(self):
        self.clear_matrix = numpy.zeros(len(self.matrix) * len(self.matrix[0]), int).reshape(len(self.matrix), len(self.matrix[0]))

    def get_shape(self):
        self.coordinate = []
        self.centre_x = 0
        self.centre_y = 0
        for y in enumerate(self.matrix):
            for x in enumerate(y[1]):
                if x[1]:
                    self.coordinate.append([x[0], y[0]])
                    self.centre_all[0].append(x[0])
                    self.centre_all[1].append(y[0])
        self.centre_x = int(round(sum(self.centre_all[0]) / len(self.centre_all[0]), 0))
        self.centre_y = int(round(sum(self.centre_all[1]) / len(self.centre_all[1]), 0))

    def create_a(self):
        self.get_shape()
        self.create_clear_matrix()
        for y, x in self.coordinate:
            x1 = (x - self.centre_x) * math.cos(self.a) - (y - self.centre_y) * math.sin(self.a) + self.centre_x
            y1 = (x - self.centre_x) * math.sin(self.a) + (y - self.centre_y) * math.cos(self.a) + self.centre_y
            self.clear_matrix[int(round(y1, 0))][int(round(x1, 0))] = 7
            self.matrix = self.clear_matrix
        [print(line) for line in self.clear_matrix]


if __name__ == '__main__':
    matrix_false = numpy.zeros(900, int).reshape((30, 30))
    matrix_anything = matrix_false.copy()
    matrix_anything[10:21, 10:21] = numpy.array([1 for _ in range(121)], int).reshape(11, 11)
    a = Rotator(matrix_anything, 341)

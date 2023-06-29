import random
from drawer import draw_map
import numpy

class MapGeneration:
    def __init__(self, wieght, hight, quantity_of_points):  # quantity_of_points = [(50, 6)]  50 == %, 6 == quality
        self.width = wieght
        self.hight = hight
        self.quantity_of_points = quantity_of_points
        self.point_sizes = list()
        self.game_map = list()
        self.array_of_true = numpy.array([True] * (self.hight * self.width)).reshape(self.hight, self.width)
        self.array_of_false = numpy.array([False] * (self.hight * self.width)).reshape(self.hight, self.width)
        self.layout_basic_map = list()  # [[x, y, scale]...]
        self.counter_names = 1

    def cor_coor(self, status, coords, scale, point=0):
        if status == 'y':
            min_y = coords - scale - point if coords - scale - point >= 0 else 0
            max_y = coords + scale + point if coords + scale + point < self.hight else (self.hight - 1)
            return (min_y, max_y)
        elif status == 'x':
            min_x = coords - scale - point if coords - scale - point >= 0 else 0
            max_x = coords + scale + point if coords + scale + point < self.width else (self.width - 1)
            return (min_x, max_x)

    def clear_map_create(self):
        self.game_map = numpy.zeros(self.hight * self.width).reshape(self.hight, self.width)

    def calculate_points(self):
        def create_point(percent, width, hight):
            return ((width * hight * (percent / 100)) ** 0.5) // 2

        created_points = [[int(create_point(point[0], self.width, self.hight))] * point[1] for point in self.quantity_of_points]
        [[self.point_sizes.append(point_2_level) if point_2_level else False for point_2_level in point_1_level] for point_1_level in created_points]

    def completion(self, width, hight, scale, name):
        xs = self.cor_coor('x', width, scale)
        ys = self.cor_coor('y', hight, scale)
        self.game_map[ys[0]: ys[1], xs[0]: xs[1]] = numpy.array([name] * ((xs[1] - xs[0]) * (ys[1] - ys[0]))).reshape((ys[1] - ys[0]), (xs[1] - xs[0]))

    def arrangement(self):
        point = self.point_sizes[0]
        layout_basic = numpy.array([False] * (self.hight * self.width)).reshape(self.hight, self.width)
        layout_basic[point: - point, point: - point] = numpy.array([True] * ((self.hight - point * 2) * (self.width - point * 2))).reshape((self.hight - point * 2), (self.width - point * 2))
        for x, y, s in self.layout_basic_map:
            xs = self.cor_coor('x', x, s, point=point)
            ys = self.cor_coor('y', y, s, point=point)
            layout_basic[ys[0]: ys[1], xs[0]: xs[1]] = self.array_of_false[ys[0]: ys[1], xs[0]: xs[1]]
        for_choice_list = []
        for y, h in enumerate(layout_basic):
            for x, w in enumerate(h):
                for_choice_list.append((x, y)) if layout_basic[y][x] else False
        if for_choice_list:
            random_choice = random.choice(for_choice_list)
            self.completion(random_choice[0], random_choice[1], point, self.counter_names)
            self.layout_basic_map.append([random_choice[0], random_choice[1], point])
        self.point_sizes.pop(0)
        self.counter_names += 1


    def main(self):
        self.calculate_points()
        self.clear_map_create()
        for _ in range(len(self.point_sizes)):
            self.arrangement()
        return self.game_map


if __name__ == '__main__':
    new_map = MapGeneration(200, 200, [(10, 4), (5, 3), (3, 1)])
    create = new_map.main()

    colors = []
    [[colors.append(j) if j not in colors else False for j in i] for i in create]
    colors_dict = {}
    for i in colors:
        if i not in colors_dict:
            colors_dict[i] = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

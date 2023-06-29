import random
from drawer import draw_map

class MapGeneration:
    def __init__(self, wieght, hight, quantity_of_points):
        self.wieght = wieght
        self.hight = hight
        self.quantity_of_points = quantity_of_points
        self.fake_point_sizes = []
        self.point_sizes = []
        self.game_map = list()
        self.counter_names = 1
        self.last_position = []
        self.cache = []
        self.cache_temporary = []
        self.cache_temporary_temporary = []

    def clear_map_create(self):
        self.game_map = [[0 for _ in range(self.wieght)] for _ in range(self.hight)]

    def random_point_create(self):
        point = random.randint(0, (self.wieght * self.hight))
        self.game_map[point // len(self.game_map)][point % len(self.game_map)] = self.counter_names
        self.counter_names += 1
        self.last_position = [point // self.hight, point % self.hight - 1]

    def calculate_points(self):
        def create_point(size, wieght, hight):
            return (((wieght // size) + (hight // size)) // 2) // 2

        created_points = [create_point(4, self.wieght, self.hight)] * self.quantity_of_points[0]\
                     + [create_point(6, self.wieght, self.hight)] * self.quantity_of_points[1]\
                     + [create_point(8, self.wieght, self.hight)] * self.quantity_of_points[2]
        self.point_sizes = created_points
        self.fake_point_sizes = created_points

    def completion(self, status, wieght, hight, counter=1):
        break_point = False
        whi_le = self.point_sizes[0] if status == 'real' else self.fake_point_sizes[0]
        while whi_le != 0:
            for r in range(len(self.game_map)):
                if r in range(hight - counter, sum([hight, counter, 1])):
                    for c in range(len(self.game_map[0])):
                        if c in range(wieght - counter, sum([wieght, counter, 1])):
                            self.cache_temporary_temporary.append([r, c])
                            if status == 'real':
                                if self.game_map[r][c] == 0:
                                    self.game_map[r][c] = self.counter_names

                            elif status == 'fake':
                                if self.game_map[r][c] != 0:
                                    break_point = True
            whi_le -= 1
            counter += 1
        if status == 'fake':
            if break_point:
                return False
            return True

    def the_chopper(self):
        def optimization(axis, value):
            true_axis = {'wieght': self.wieght, 'hight': self.hight}
            if value < 0:
                value *= -1
            if true_axis[axis] == self.wieght and value >= self.wieght:
                value = value % self.wieght
            if true_axis[axis] == self.hight and value >= self.hight:
                value = value % self.hight
            return value
        break_point = 0
        while break_point != 500:
            break_point += 1
            random_point = (random.randint(0, self.wieght), random.randint(0, self.hight))
            true_gorizontal, true_vertical = optimization('wieght', random_point[0]), optimization('hight', random_point[1])
            if self.point_sizes:
                prove_collision = self.completion('fake', true_gorizontal, true_vertical)
                if ([true_gorizontal, true_vertical] not in self.cache) and \
                    ((true_vertical + self.point_sizes[0] + 1) <= self.wieght) and (
                    (true_gorizontal + self.point_sizes[0] + 1) <= self.hight) and (
                    true_vertical - self.point_sizes[0] >= 0) and (true_gorizontal - self.point_sizes[0] >= 0) and \
                    prove_collision:
                    self.game_map[true_vertical][true_gorizontal] = self.counter_names
                    self.completion('real', true_gorizontal, true_vertical)
                    # line(desired_point[0], true_gorizontal, desired_point[1], true_vertical, game_map, counter + 1)
                    self.fake_point_sizes.pop(0)
                    self.counter_names += 1
                    self.cache_temporary.append(self.cache_temporary_temporary)
                    self.cache.append(self.cache_temporary)
                else:
                    self.cache_temporary_temporary = []
    def map_create(self):
        self.calculate_points()
        self.clear_map_create()
        self.random_point_create()
        for _ in range(len(self.point_sizes)):
            self.the_chopper()
        return self.game_map


new_map = MapGeneration(100, 100, [5, 5, 15])
create = new_map.map_create()



colors = []
[[colors.append(j) if j not in colors else False for j in i] for i in create]
colors_dict = {}
for i in colors:
    if i not in colors_dict:
        colors_dict[i] = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

draw_map(colors_dict, create, 100, 100)
#





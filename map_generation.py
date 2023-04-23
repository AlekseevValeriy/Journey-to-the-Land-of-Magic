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
        prove_list = []
        for y in enumerate(self.game_map):
            for x in enumerate(y[1]):
                prove = self.completion('fake', x[0], y[0])
                if prove:
                    prove_list.append([x[0], y[0]])
        if prove_list:
            print(prove_list)
            random_proved_point = random.choice(prove_list)
            self.completion('real', random_proved_point[0], random_proved_point[1])
        self.fake_point_sizes.pop(0)
        self.counter_names += 1
        return

    def map_create(self):
        self.calculate_points()
        self.clear_map_create()
        self.random_point_create()
        for _ in range(len(self.point_sizes)):
            self.the_chopper()
        return self.game_map


new_map = MapGeneration(100, 100, [3, 3, 15])
create = new_map.map_create()



colors = []
[[colors.append(j) if j not in colors else False for j in i] for i in create]
colors_dict = {}
for i in colors:
    if i not in colors_dict:
        colors_dict[i] = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

draw_map(colors_dict, create, 100, 100)
#





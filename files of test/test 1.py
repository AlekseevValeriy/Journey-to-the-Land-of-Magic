"""v1"""


def the_chopper(self):
    def optimization(axis, value):
        true_axis = {'wieght': self.width, 'hight': self.hight}
        if value < 0:
            value *= -1
        if true_axis[axis] == self.width and value >= self.width:
            value = value % self.width
        if true_axis[axis] == self.hight and value >= self.hight:
            value = value % self.hight
        return value

    break_point = 0
    while True:
        new_random_point = [self.last_position[0] + (random.randint(1, 20) * random.choice([-1, 1])),
                            self.last_position[1] + (random.randint(1, 20) * random.choice([-1, 1]))]
        true_gorizontal = optimization('wieght', new_random_point[0])
        true_vertical = optimization('hight', new_random_point[1])
        prove_collision = self.completion('fake', true_gorizontal, true_vertical)
        break_point += 1
        if break_point == 100:
            break
        if ((true_vertical + self.point_sizes[0] + 1) <= self.width) and (
                (true_gorizontal + self.point_sizes[0] + 1) <= self.hight) and (
                true_vertical - self.point_sizes[0] >= 0) and (
                true_gorizontal - self.point_sizes[0] >= 0) and prove_collision:
            self.game_map[true_vertical][true_gorizontal] = self.counter_names
            self.completion('real', true_gorizontal, true_vertical)
            # line(desired_point[0], true_gorizontal, desired_point[1], true_vertical, game_map, counter + 1)
            self.fake_point_sizes.pop(0)
            self.last_position = [true_vertical, true_gorizontal]
            self.counter_names += 1
            return


"""v2"""


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


"""v3"""


def optimization(axis, value):
    true_axis = {'wieght': self.width, 'hight': self.hight}
    if value < 0:
        value *= -1
    if true_axis[axis] == self.width and value >= self.width:
        value = value % self.width
    if true_axis[axis] == self.hight and value >= self.hight:
        value = value % self.hight
    return value


break_point = 0
while break_point != 500:
    break_point += 1
    random_point = (random.randint(0, self.width), random.randint(0, self.hight))
    true_gorizontal, true_vertical = optimization('wieght', random_point[0]), optimization('hight', random_point[1])
    if self.point_sizes:
        prove_collision = self.completion('fake', true_gorizontal, true_vertical)
        if ([true_gorizontal, true_vertical] not in self.cache) and \
                ((true_vertical + self.point_sizes[0] + 1) <= self.width) and (
                (true_gorizontal + self.point_sizes[0] + 1) <= self.hight) and (
                true_vertical - self.point_sizes[0] >= 0) and (true_gorizontal - self.point_sizes[0] >= 0) and \
                prove_collision:
            self.game_map[true_vertical][true_gorizontal] = self.counter_names
            self.completion('real', true_gorizontal, true_vertical)
            self.fake_point_sizes.pop(0)
            self.counter_names += 1
            self.cache_temporary.append(self.cache_temporary_temporary)
            self.cache.append(self.cache_temporary)
        else:
            self.cache_temporary_temporary = []
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
    while True:
        new_random_point = [self.last_position[0] + (random.randint(1, 20) * random.choice([-1, 1])),
                            self.last_position[1] + (random.randint(1, 20) * random.choice([-1, 1]))]
        true_gorizontal = optimization('wieght', new_random_point[0])
        true_vertical = optimization('hight', new_random_point[1])
        prove_collision = self.completion('fake', true_gorizontal, true_vertical)
        break_point += 1
        if break_point == 100:
            break
        if ((true_vertical + self.point_sizes[0] + 1) <= self.wieght) and (
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
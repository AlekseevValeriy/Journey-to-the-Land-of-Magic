import random
from drawer import draw_map

def completion(name, wieght, hight, scale, game_map, status, counter=1):  # наполнение
    break_point = False
    collision_new = []
    while scale != 0:
        for r in range(len(game_map)):
            if r in range(hight - counter, sum([hight, counter, 1])):
                for c in range(len(game_map[0])):
                    if c in range(wieght - counter, sum([wieght, counter, 1])):
                        if status == 'real':
                            if game_map[r][c] == 0:
                                game_map[r][c] = name
                        elif status == 'fake':
                            if game_map[r][c] == 0:
                                collision_new.append((r, c))
                            else:
                                break_point = True
        scale -= 1
        counter += 1
    if status == 'real':
        return game_map
    elif status == 'fake':
        if break_point:
            return False
        return list(set(collision_new))


def generate_clear_map(wieght, hight):
    game_map = [[0 for _ in range(wieght)] for _ in range(hight)]
    return game_map


def random_point(wieght, hight, game_map, counter):
    new_game_map = game_map[:]
    point = random.randint(0, (wieght * hight))
    new_game_map[point // hight][point % hight - 1] = counter
    position = [point // hight, point % hight - 1]
    return new_game_map, position, counter + 1


def calculate_points(wieght, hight, quantity):
    def big_point(wieght_1, hight_1):
        return (((wieght_1 // 4) + (hight_1 // 4)) // 2) // 2

    def medium_point(wieght_2, hight_2):
        return (((wieght_2 // 6) + (hight_2 // 6)) // 2) // 2

    def small_point(wieght_3, hight_3):
        return (((wieght_3 // 8) + (hight_3 // 8)) // 2) // 2

    new_points = [big_point(wieght, hight)] * quantity[0] + [medium_point(wieght, hight)] * quantity[1] + [
        small_point(wieght, hight)] * quantity[2]
    return new_points


def the_chopper(desired_point, wieght, hight, game_map, counter, scale):
    new_game_map = game_map[:]

    def optimization(axis, value):
        true_axis = {'wieght': wieght, 'hight': hight}
        if value < 0:
            value *= -1
        if true_axis[axis] == wieght and value >= wieght:
            value = value % wieght
        if true_axis[axis] == hight and value >= hight:
            value = value % hight
        return value

    while True:
        vertical = random.choice([-1, 1])
        gorizontal = random.choice([-1, 1])
        vertical_len = random.randint(1, 20)
        gorizontal_len = random.randint(1, 20)
        new_random_point = [desired_point[0] + (gorizontal_len * gorizontal),
                            desired_point[1] + (vertical_len * vertical)]
        true_gorizontal = optimization('wieght', new_random_point[0])
        true_vertical = optimization('hight', new_random_point[1])
        prove_collision = completion(counter, true_gorizontal, true_vertical, scale, new_game_map, 'fake')
        if ((true_vertical + scale + 1) <= wieght) and ((true_gorizontal + scale + 1) <= hight) and (
                true_vertical - scale >= 0) and (true_gorizontal - scale >= 0) and prove_collision:
            new_game_map[true_vertical][true_gorizontal] = counter
            completion(counter, true_gorizontal, true_vertical, scale, new_game_map, 'real')
            position = [true_vertical, true_gorizontal]
            # line(desired_point[0], true_gorizontal, desired_point[1], true_vertical, game_map, counter + 1)
            return new_game_map, position, counter + 1











points = calculate_points(25, 25, [2, 6, 8])
random_point_new = random_point(25, 25, generate_clear_map(25, 25), 1)
new_point = the_chopper(random_point_new[1], 25, 25, random_point_new[0][:], random_point_new[2], points[0])
for i in points[1:-2]:
    new_point = the_chopper(new_point[1], 25, 25, new_point[0][:], new_point[2], i)
new_point = the_chopper(new_point[1], 25, 25, new_point[0][:], new_point[2], points[-1])

colors = []
[[colors.append(j) if j not in colors else False for j in i] for i in new_point[0]]
colors_dict = {}
for i in colors:
    if i not in colors_dict:
        colors_dict[i] = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

draw_map(colors_dict, new_point, 500, 500)

import random
b = 40
a = [[0 for _ in range(b)]for _ in range(b)]

counter_of_side, times_on_edge, step_back = 0, 0, 0
def line(dict, start, counter_of_side, times_on_edge_real, step_back, door_step=4, times_on_edge_all=3, step_back_times=3):
    if step_back:
        if counter_of_side > 0:
            counter_of_side -= 1
        elif counter_of_side < 0:
            counter_of_side += 1
        else:
            counter_of_side += random.choice([1, -1])
        step_back -= 1
    else:
        counter_of_side += random.choice([1, -1])
    if counter_of_side > door_step:
        counter_of_side -= 1
    if counter_of_side < - door_step:
        counter_of_side += 1
    dict[start[0] + counter_of_side][start[1] + 1] = 1

    if counter_of_side == door_step:
        times_on_edge_real += 1
    else:
        times_on_edge_real = 0

    if times_on_edge_real == times_on_edge_all:
        step_back = step_back_times
    return counter_of_side, times_on_edge_real, step_back

for n in range(25):
    counter_of_side, times_on_edge, step_back = line(a, [30, 3 + n], counter_of_side, times_on_edge, step_back)

[print(i) for i in a]
# TODO перенеси это в вг 2
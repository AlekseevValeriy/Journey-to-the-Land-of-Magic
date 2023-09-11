class LineDrawer:

    def ant_line(self, dict, start, finish, side, inverse=False, door_step=2, sign=1):
        from random import choice
        # sign = 1

        def line(counter_of_side, times_on_edge_real, step_back, door_step, times_on_edge_all=3, step_back_times=3):
            if step_back:
                pass
                # if counter_of_side > 0:
                #     counter_of_side -= 1
                # elif counter_of_side < 0:
                #     counter_of_side += 1
                # else:
                #     counter_of_side += choice([1, -1])
                # step_back -= 1
            else:
                counter_of_side += choice([1, -1])
            if counter_of_side > door_step:
                counter_of_side = door_step
            if counter_of_side < - door_step:
                counter_of_side = - door_step

            # if counter_of_side == door_step:
            #     times_on_edge_real += 1
            # else:
            #     times_on_edge_real = 0
            #
            # if times_on_edge_real == times_on_edge_all:
            #     step_back = step_back_times
            return counter_of_side, times_on_edge_real, step_back

        counter_of_side, times_on_edge, step_back = 0, 0, 0
        for i in range(abs(start[1] - finish[1]) if side == 'v' else abs(start[0] - finish[0])):
            counter_of_side, times_on_edge, step_back = line(counter_of_side, times_on_edge, step_back, door_step)

            for j in range(abs(counter_of_side)):
                j = j if counter_of_side >= 0 else - j
                if side == 'v':
                    dict[start[1] + i][start[0] + j] = 3
                else:
                    dict[start[1] + j][start[0] + i] = 3

            for j in range(abs(counter_of_side)):
                j = j if counter_of_side >= 0 else - j
                if side == 'v':
                    if inverse:
                        number = sign if start[0] + j >= start[0] and dict[start[1] + i][start[0] + j - 1] in [sign, 0] else 0
                    else:
                        number = sign if start[0] + j <= start[0] and dict[start[1] + i][start[0] + j + 1] in [sign, 0] else 0
                    dict[start[1] + i][start[0] + j] = number
                else:
                    if inverse:
                        number = sign if start[1] + j >= start[1] and dict[start[1] + j - 1][start[0] + i] in [sign, 0] else 0
                    else:
                        number = sign if start[1] + j <= start[1] and dict[start[1] + j + 1][start[0] + i] in [sign, 0] else 0
                    dict[start[1] + j][start[0] + i] = number


if __name__ == '__main__':
    from numpy import zeros, ones

    dict = zeros((24, 24), dtype='int32')
    dict[4:19, 5: 20] = ones((15, 15), dtype='int32')
    # dict = [[(str(j[1]), j[0], i[0]) for j in enumerate(i[1])] for i in enumerate(dict)]
    LineDrawer().ant_line(dict, [5, 4], [19, 4], 'g', inverse=False)
    LineDrawer().ant_line(dict, [19, 4], [19, 18], 'v', inverse=True)
    LineDrawer().ant_line(dict, [5, 18], [19, 18], 'g', inverse=True)
    LineDrawer().ant_line(dict, [5, 4], [5, 18], 'v', inverse=False)
    [print(*line) for line in dict]

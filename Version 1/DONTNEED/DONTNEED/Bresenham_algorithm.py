def line(x0, x1, y0, y1, my_place, symbol):
    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    error = 0
    delta_err = (delta_y + 1) / (delta_x + 1)
    y = y0
    dir_y = y1 - y0
    if dir_y > 0:
        dir_y = 1
    if dir_y < 0:
        dir_y = -1
    for x in range(x0, x1):
        my_place[y][x] = symbol
        error = error + delta_err
        if error >= 1.0:
            y = y + dir_y
            error = error - 1.0

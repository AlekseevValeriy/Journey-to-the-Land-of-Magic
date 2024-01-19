from random import choice
from typing import Callable


class LineDrawer:
    '''Класс рисования линии в листе'''
    def __init__(self) -> None:
        self.add_length = 0

    def bresenham_line(self, x1=0, y1=0, x2=0, y2=0) -> list:
        '''Метод рисование линии по алгоритму Бресенхама'''
        coordinates = []
        dx = x2 - x1
        dy = y2 - y1
        sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
        if dx < 0:
            dx = -dx
        if dy < 0:
            dy = -dy
        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy
        x, y = x1, y1
        error, t = el / 2, 0
        coordinates.append([x, y])
        while t < el:
            error -= es
            if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1
            coordinates.append([x, y])
        return coordinates

    def mandatory_cleaning(func: Callable):
        '''Декоратор очистки длины'''
        def fun(self, *args, **kwargs):
            self.add_length = 0
            func(self, *args, **kwargs)
            self.add_length = 0
        return fun

    @mandatory_cleaning
    def ant_line(self, matrix, start, finish, side, inverse=False, to_edge=2, symbol=1, markup_symbol=-1) -> None:
        '''Метод рисования кривой линии на листе'''
        def line_change():
            self.add_length += choice([-1, 1])
            self.add_length = to_edge if self.add_length > to_edge else self.add_length
            self.add_length = - to_edge if self.add_length < - to_edge else self.add_length

        for i in range(abs(start[1] - finish[1] if side == 'v' else start[0] - finish[0])):
            line_change()

            for j in range(abs(self.add_length)):
                j = j if self.add_length >= 0 else - j
                if not inverse:
                    temporary_symbol = symbol if self.add_length < 0 else 0
                else:
                    temporary_symbol = symbol if self.add_length >= 0 else 0
                if side == 'v':
                    matrix[start[1] + i][start[0] + j] = temporary_symbol
                else:
                    matrix[start[1] + j][start[0] + i] = temporary_symbol

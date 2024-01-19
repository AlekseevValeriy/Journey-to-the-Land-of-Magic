from random import random, choice
from numpy import array, ndarray


class CellularAutomata:
    '''Класс генерации подземелья'''
    FLOOR = 1
    WALL = 0
    WOOD = 20
    EMPTY = -1

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.grid = None

        self.chance_to_start_alive = 0.4
        self.death_limit = 3
        self.birth_limit = 4
        self.number_of_steps = 4

        self.grid = self.create_grid()
        self.initialize_grid()
        for step in range(self.number_of_steps):
            self.grid = self.do_simulation_step()


    def create_grid(self) -> list:
        return [[CellularAutomata.WALL for _x in range(self.width)] for _y in range(self.height)]

    def initialize_grid(self) -> None:
        for row in range(self.height):
            for column in range(self.width):
                if random() <= self.chance_to_start_alive:
                    self.grid[row][column] = CellularAutomata.FLOOR

    def count_alive_neighbors(self, x: int, y: int) -> int:
        alive_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x = x + i
                neighbor_y = y + j
                if i == 0 and j == 0:
                    continue
                elif neighbor_x < 0 or neighbor_y < 0 or neighbor_y >= self.height or neighbor_x >= self.width:
                    alive_count += 1
                elif self.grid[neighbor_y][neighbor_x] == CellularAutomata.FLOOR:
                    alive_count += 1
        return alive_count

    def do_simulation_step(self) -> list:
        new_grid = self.create_grid()
        for x in range(self.width):
            for y in range(self.height):
                alive_neighbors = self.count_alive_neighbors(x, y)
                if self.grid[y][x] == CellularAutomata.FLOOR:
                    if alive_neighbors < self.death_limit:
                        new_grid[y][x] = CellularAutomata.WALL
                    else:
                        new_grid[y][x] = CellularAutomata.FLOOR
                else:
                    if alive_neighbors > self.birth_limit:
                        new_grid[y][x] = CellularAutomata.FLOOR
                    else:
                        new_grid[y][x] = CellularAutomata.WALL
        return new_grid

    def set_item(self) -> list:
        layout = []
        places = []
        for n, line in enumerate(self.grid):
            layout.append([])
            for m, element in enumerate(line):
                if not element:
                    places.append((m, n))
                layout[n].append(CellularAutomata.EMPTY)
        place = choice(places)
        layout[place[1]][place[0]] = CellularAutomata.WOOD

        return layout

    def get_map(self) -> ndarray:
        return array([self.grid, self.set_item()])

    def __str__(self):
        return '\n'.join((''.join(tuple(map(str, line))) for line in self.grid))

    def __iter__(self):
        for layer in self.grid:
            for line in layer:
                yield ' '.join(tuple(map(str, line))) + '\n'

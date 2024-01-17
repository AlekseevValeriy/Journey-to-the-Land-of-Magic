import random
import numpy


class CellularAutomata:
    FLOOR = 1
    WALL = 0
    WOOD = 2
    EMPTY = -1

    def __init__(self, width, height):
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

    def create_grid(self):
        return [[CellularAutomata.WALL for _x in range(self.width)] for _y in range(self.height)]

    def initialize_grid(self):
        for row in range(self.height):
            for column in range(self.width):
                if random.random() <= self.chance_to_start_alive:
                    self.grid[row][column] = CellularAutomata.FLOOR

    def count_alive_neighbors(self, x, y):
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

    def do_simulation_step(self):
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

    def set_item(self):
        layout = self.grid.copy()
        places = []
        for n, line in enumerate(layout):
            for m, element in enumerate(line):
                if not element:
                    places.append((n, m))
                layout[n][m] = CellularAutomata.EMPTY
        place = random.choice(places)
        layout[place[1]][place[0]] = CellularAutomata.WOOD

        return layout

    def get_map(self):
        return numpy.array([self.grid, self.set_item()])

    def __str__(self):
        return '\n'.join((''.join(tuple(map(str, line))) for line in self.grid))

    def __iter__(self):
        for line in self.grid:
            yield ' '.join(tuple(map(str, line))) + '\n'


if __name__ == '__main__':
    generator = CellularAutomata(50, 25)
    print(generator)

    print(*generator)

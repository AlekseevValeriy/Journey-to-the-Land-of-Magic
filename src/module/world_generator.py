import pygame

from line_drawer import LineDrawer
import numpy
from pygame.image import load
import random
from cellular_automata import CellularAutomata

class WorldGenerator:
    '''Класс генератора мира'''
    def __init__(self, size=(100, 100)) -> None:
        self.world_layout = numpy.array([])
        self.width, self.height = size
        self.textures = {0: 'empty', 1: 'texture_1', 2: 'texture_2', 3: 'texture_3', 4: 'texture_4',
                         5: 'texture_5', 10: 'grass', 12: 'door', 13: 'boat', 20: 'sphere'}
        # 1 -> (51, 51, 51), 2 -> (102, 102, 102), 3 -> (128, 128, 128), 4 -> (153, 153 153),
        # 5 -> (179, 179, 179), 10 -> (204, 204, 204), 12 -> (220, 220, 220), 13 -> (135, 135, 135)
        self.set_textures()
        self.doors_coordinate = ()

    def set_textures(self) -> None:
        '''Метод для установки текстур'''
        texture_name = self.textures
        self.textures = {}
        for name in texture_name:
            if texture_name[name]:
                self.textures[name] = load(f"../../data/textures/world/{texture_name[name]}.png").convert_alpha()

    def texturing_process(self, world_element: int) -> pygame.Surface:
        '''Метод процесса установки текстур'''
        return self.textures.get(world_element, False)

    def texturing(self, world: numpy.ndarray) -> numpy.ndarray:
        '''Метод для текстурирования'''
        a = world[:]
        for r, z in enumerate(world):
            for n, y in enumerate(z):
                for m, x in enumerate(y):
                    a[r][n][m] = self.textures.get(x, False)
        return a

    def create_field(self, world_frame=10, external_frame=8, regions=[2, 3, 4, 5]) -> numpy.ndarray:
        '''Метод для создания земли'''
        regions = [2, 3, 4, 5]
        door_step_ocean = 3
        world_layout = numpy.zeros((world_frame * 2 + self.height, world_frame * 2 + self.width), dtype='int32')
        island_layout = numpy.ones((self.height, self.width), dtype='int32')
        world_layout[world_frame: world_frame + self.height, world_frame: world_frame + self.width] = island_layout
        line_dr = LineDrawer()
        line_dr.ant_line(world_layout, [world_frame, world_frame], [world_frame + self.width, world_frame], 'g',
                         to_edge=door_step_ocean)
        line_dr.ant_line(world_layout, [world_frame + self.width, world_frame],
                         [world_frame + self.width, world_frame + self.height], 'v', inverse=True,
                         to_edge=door_step_ocean)
        line_dr.ant_line(world_layout, [world_frame, world_frame + self.height],
                         [world_frame + self.width, world_frame + self.height], 'g', inverse=True,
                         to_edge=door_step_ocean)
        line_dr.ant_line(world_layout, [world_frame, world_frame], [world_frame, world_frame + self.height], 'v',
                         to_edge=door_step_ocean)
        one_x = 0
        lh_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2),
                                dtype='int32')
        x = random.choice(regions)
        one_x = x
        regions.remove(x)
        lh_sector_full = numpy.array([[x for _ in range(external_frame * 2 + self.width // 2)] for _ in
                                      range(external_frame + self.height // 2)])
        lh_sector[0: external_frame + self.height // 2, 0: external_frame * 2 + self.width // 2] = lh_sector_full
        line_dr.ant_line(lh_sector, [0, external_frame + self.height // 2],
                         [external_frame * 2 + self.width // 2, external_frame + self.height // 2], 'g',
                         to_edge=door_step_ocean, symbol=x, inverse=True)

        ld_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2),
                                dtype='int32')
        x = random.choice(regions)
        regions.remove(x)
        ld_sector_full = numpy.array([[x for _ in range(external_frame + self.width // 2)] for _ in
                                      range(external_frame * 2 + self.height // 2)])
        ld_sector[0: external_frame * 2 + self.height // 2, 0: external_frame + self.width // 2] = ld_sector_full
        line_dr.ant_line(ld_sector, [external_frame + self.width // 2, 0],
                         [external_frame + self.width // 2, external_frame * 2 + self.height // 2], 'v',
                         to_edge=door_step_ocean, symbol=x, inverse=True)

        rd_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2),
                                dtype='int32')
        x = random.choice(regions)
        regions.remove(x)
        rd_sector_full = numpy.array([[x for _ in range(external_frame * 2 + self.width // 2)] for _ in
                                      range(external_frame + self.height // 2)])
        rd_sector[external_frame: external_frame * 2 + self.height // 2,
        0: external_frame * 2 + self.width // 2] = rd_sector_full
        line_dr.ant_line(rd_sector, [0, external_frame], [external_frame + self.width // 2, external_frame], 'g',
                         to_edge=door_step_ocean, symbol=x)

        rh_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2),
                                dtype='int32')
        x = random.choice(regions)
        regions.remove(x)
        rh_sector_full = numpy.array([[x for _ in range(external_frame + self.width // 2)] for _ in
                                      range(external_frame * 2 + self.height // 2)])
        rh_sector[0: external_frame * 2 + self.height // 2,
        external_frame: external_frame * 2 + self.width // 2] = rh_sector_full
        line_dr.ant_line(rh_sector, [external_frame, 0], [external_frame, external_frame + self.height // 2], 'v',
                         to_edge=door_step_ocean, symbol=x)

        center_sector = numpy.zeros((external_frame * 2 + self.height // 3, external_frame * 2 + self.width // 3),
                                    dtype='int32')
        center_sector_full = numpy.ones((self.height // 3, self.width // 3))
        center_sector[external_frame: external_frame + self.height // 3,
        external_frame: external_frame + self.width // 3] = center_sector_full
        line_dr.ant_line(center_sector, [external_frame, external_frame],
                         [external_frame + self.width // 3, external_frame], 'g', to_edge=door_step_ocean, symbol=1)
        line_dr.ant_line(center_sector, [external_frame, external_frame],
                         [external_frame, external_frame + self.height // 3], 'v', to_edge=door_step_ocean, symbol=1)
        line_dr.ant_line(center_sector, [external_frame, external_frame + self.height // 3],
                         [external_frame + self.width // 3, external_frame + self.height // 3], 'g',
                         to_edge=door_step_ocean, symbol=1, inverse=True)
        line_dr.ant_line(center_sector, [external_frame + self.width // 3, external_frame],
                         [external_frame + self.width // 3, external_frame + self.height // 3], 'v',
                         to_edge=door_step_ocean, symbol=1, inverse=True)

        beach_size = 6
        beach_door_step = 3
        beach_donut = numpy.ones((external_frame * 2 + self.height, external_frame * 2 + self.width), dtype='int32')
        beach_abyss = numpy.zeros((self.height - beach_size * 2, self.width - beach_size * 2), dtype='int32')
        beach_donut[external_frame + beach_size: external_frame + self.height - beach_size,
        external_frame + beach_size: external_frame + self.width - beach_size] = beach_abyss
        line_dr.ant_line(beach_donut, [external_frame + beach_size, external_frame + beach_size],
                         [external_frame + self.width - beach_size, external_frame + beach_size], 'g',
                         to_edge=beach_door_step, symbol=6, inverse=True)
        line_dr.ant_line(beach_donut, [external_frame + beach_size, external_frame + beach_size],
                         [external_frame + beach_size, external_frame + self.height - beach_size], 'v',
                         to_edge=beach_door_step, symbol=6, inverse=True)
        line_dr.ant_line(beach_donut, [external_frame + self.width - beach_size, external_frame + beach_size],
                         [external_frame + self.width - beach_size, external_frame + self.height - beach_size], 'v',
                         to_edge=beach_door_step, symbol=6, inverse=False)
        line_dr.ant_line(beach_donut, [external_frame + beach_size, external_frame + self.height - beach_size],
                         [external_frame + self.width - beach_size, external_frame + self.height - beach_size], 'g',
                         to_edge=beach_door_step, symbol=6, inverse=False)

        for i in range(external_frame * 2 + self.height // 2):
            for j in range(external_frame * 2 + self.width // 2):
                position = world_layout[world_frame - external_frame + i][world_frame - external_frame + j]
                if position == 1 and lh_sector[i][j]:
                    world_layout[world_frame - external_frame + i][world_frame - external_frame + j] = lh_sector[i][j]

        for i in range(external_frame * 2 + self.height // 2):
            for j in range(external_frame * 2 + self.width // 2):
                position = world_layout[self.height // 2 + world_frame - external_frame + i][
                    world_frame - external_frame + j]
                if position == 1 and ld_sector[i][j]:
                    world_layout[self.height // 2 + world_frame - external_frame + i][
                        world_frame - external_frame + j] = ld_sector[i][j]

        for i in range(external_frame * 2 + self.height // 2):
            for j in range(external_frame * 2 + self.width // 2):
                position = world_layout[self.height // 2 + world_frame - external_frame + i][
                    world_frame - external_frame + j + self.width // 2]
                if position == 1 and rd_sector[i][j]:
                    world_layout[self.height // 2 + world_frame - external_frame + i][
                        world_frame - external_frame + j + self.width // 2] = rd_sector[i][j]

        for i in range(external_frame * 2 + self.height // 2):
            for j in range(external_frame * 2 + self.width // 2):
                position = world_layout[world_frame - external_frame + i][
                    world_frame - external_frame + j + self.width // 2]
                if position in [1, one_x] and rh_sector[i][j]:
                    world_layout[world_frame - external_frame + i][world_frame - external_frame + j + self.width // 2] = \
                    rh_sector[i][j]

        for i in range(external_frame * 2 + self.height // 3):
            for j in range(external_frame * 2 + self.width // 3):
                position = world_layout[world_frame - external_frame + i + self.height // 3][
                    world_frame - external_frame + j + self.width // 3]
                if position and center_sector[i][j]:
                    world_layout[world_frame - external_frame + i + self.height // 3][
                        world_frame - external_frame + j + self.width // 3] = center_sector[i][j]

        for i in range(external_frame * 2 + self.height):
            for j in range(external_frame * 2 + self.width):
                position = world_layout[world_frame - external_frame + i][world_frame - external_frame + j]
                if beach_donut[i][j] and position:
                    world_layout[world_frame - external_frame + i][world_frame - external_frame + j] = 6
        self.world_layout = world_layout

    def create_grass(self, value = 10):
        '''Метод для создания земли'''
        grass = self.world_layout.copy()
        for n, y in enumerate(self.world_layout):
            for m, x in enumerate(y):
                grass[n][m] = -1
                if x not in (6, 0):
                    if random.choice((0, 1)):
                        grass[n][m] = value
        return grass

    def set_random_player_position(self) -> list:
        '''Метод для определения позиции игрока'''
        world_max = (len(self.world_layout[0][0]) - 1, len(self.world_layout[0]) - 1)
        side = random.choice(('vertical', 'gorizontal'))
        if side == 'left':
            position = (0, random.randint(0, len(self.world_layout[0]) - 1))
        elif side == 'right':
            position = (len(self.world_layout[0][0]) - 1, random.randint(0, len(self.world_layout[0]) - 1))
        elif side == 'up':
            position = (random.randint(0, len(self.world_layout[0][0]) - 1), 0)
        elif side == 'down':
            position = (random.randint(0, len(self.world_layout[0][0]) - 1), len(self.world_layout[0]) - 1)

        if side == 'gorizontal':
            position = (0, random.randint(30, len(self.world_layout[0]) - 30))
        elif side == 'vertical':
            position = (random.randint(30, len(self.world_layout[0][0]) - 30), 0)
        position = list(position)
        points = []
        if side == 'gorizontal':
            while True:
                position[0] += 1
                if position[0] < world_max[0]:
                    if self.world_layout[0][position[1]][position[0]] != 0:
                        points.append((position[0], position[1]))
                else:
                    break
        if side  == 'vertical':
            while True:
                position[1] += 1
                if position[1] < world_max[1]:
                    if self.world_layout[0][position[1]][position[0]] != 0:
                        points.append((position[0], position[1]))
                else:
                    break
        sector_size = 100
        position = random.choice(points)
        position = (n * sector_size for n in position)
        return list(position)

    def create_objects(self) -> numpy.ndarray:
        '''Метод для создания люков'''
        objects = self.world_layout.copy()
        places = {2: [], 3: [], 4: [], 5: [], 6: []}

        for n, y in enumerate(self.world_layout):
            for m, x in enumerate(y):
                if x in places:
                    places[x].append((m, n))
                objects[n][m] = -1
        places = ((2, random.choice(places[2])), (2, random.choice(places[3])), (2, random.choice(places[4])),
                  (2, random.choice(places[5])), (3, random.choice(places[6])))
        self.doors_coordinate = (places[0][1], places[1][1], places[2][1] ,places[3][1])
        for key, item in tuple(places):
            objects[item[1]][item[0]] = key + 10

        return objects

    def create_doors(self) -> tuple:
        '''Метод для создания подземелий'''
        door_1 = CellularAutomata(random.randint(40, 60), random.randint(40, 60)).get_map().tolist()
        door_2 = CellularAutomata(random.randint(40, 60), random.randint(40, 60)).get_map().tolist()
        door_3 = CellularAutomata(random.randint(40, 60), random.randint(40, 60)).get_map().tolist()
        door_4 = CellularAutomata(random.randint(40, 60), random.randint(40, 60)).get_map().tolist()

        return door_1, door_2, door_3, door_4


    def create_world(self) -> None:
        '''Метод для создания мира'''
        self.create_field()
        plot: numpy.ndarray = self.world_layout.copy()

        grass: numpy.ndarray = self.create_grass()
        objects: numpy.ndarray = self.create_objects()
        self.world_layout = numpy.array([plot, grass, objects]).tolist()


    def get_world(self) -> numpy.ndarray:
        '''Метод, возвращающий мир'''
        return self.world_layout



    def get_doors(self) -> dict:
        '''Метод, возвращающий подземелья'''
        doors = self.create_doors()
        doors_dict = {}
        for position, door in zip(self.doors_coordinate, doors):
            doors_dict[str(position[0]) + str(position[1])] = door
        return doors_dict
import os
import random

import numpy
import pygame
from PIL import Image

"""
Класс, который процедурно генерирует игровой мир
"""


class WorldGenerator:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.world_layout = []

    def create_world_layout(self, world_frame=10, external_frame=8, regions=[2, 3, 4, 5]):
        from line_drawer import LineDrawer
        door_step_ocean = 3
        world_layout = numpy.zeros((world_frame * 2 + self.height, world_frame * 2 + self.width), dtype='int32')
        island_layout = numpy.ones((self.height, self.width), dtype='int32')
        world_layout[world_frame: world_frame + self.height, world_frame: world_frame + self.width] = island_layout
        line_dr = LineDrawer()
        line_dr.ant_line(world_layout, [world_frame, world_frame], [world_frame + self.width, world_frame], 'g', to_edge=door_step_ocean)
        line_dr.ant_line(world_layout, [world_frame + self.width, world_frame], [world_frame + self.width, world_frame + self.height], 'v', inverse=True, to_edge=door_step_ocean)
        line_dr.ant_line(world_layout, [world_frame, world_frame + self.height], [world_frame + self.width, world_frame + self.height], 'g', inverse=True, to_edge=door_step_ocean)
        line_dr.ant_line(world_layout, [world_frame, world_frame], [world_frame, world_frame + self.height], 'v', to_edge=door_step_ocean)
        one_x = 0
        lh_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2), dtype='int32')
        x = random.choice(regions)
        one_x = x
        regions.remove(x)
        lh_sector_full = numpy.array([[x for _ in range(external_frame * 2 + self.width // 2)] for _ in range(external_frame + self.height // 2)])
        lh_sector[0: external_frame + self.height // 2, 0: external_frame * 2 + self.width // 2] = lh_sector_full
        line_dr.ant_line(lh_sector, [0, external_frame + self.height // 2], [external_frame * 2 + self.width // 2, external_frame + self.height // 2], 'g', to_edge=door_step_ocean, symbol=x, inverse=True)

        ld_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2), dtype='int32')
        x = random.choice(regions)
        regions.remove(x)
        ld_sector_full = numpy.array([[x for _ in range(external_frame + self.width // 2)] for _ in range(external_frame * 2 + self.height // 2)])
        ld_sector[0: external_frame * 2 + self.height // 2, 0: external_frame + self.width // 2] = ld_sector_full
        line_dr.ant_line(ld_sector, [external_frame + self.width // 2, 0], [external_frame + self.width // 2, external_frame * 2 + self.height // 2], 'v', to_edge=door_step_ocean, symbol=x, inverse=True)

        rd_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2), dtype='int32')
        x = random.choice(regions)
        regions.remove(x)
        rd_sector_full = numpy.array([[x for _ in range(external_frame * 2 + self.width // 2)] for _ in range(external_frame + self.height // 2)])
        rd_sector[external_frame: external_frame * 2 + self.height // 2, 0: external_frame * 2 + self.width // 2] = rd_sector_full
        line_dr.ant_line(rd_sector, [0, external_frame], [external_frame + self.width // 2, external_frame], 'g', to_edge=door_step_ocean, symbol=x)

        rh_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2), dtype='int32')
        x = random.choice(regions)
        regions.remove(x)
        rh_sector_full = numpy.array([[x for _ in range(external_frame + self.width // 2)] for _ in range(external_frame * 2 + self.height // 2)])
        rh_sector[0: external_frame * 2 + self.height // 2, external_frame: external_frame * 2 + self.width // 2] = rh_sector_full
        line_dr.ant_line(rh_sector, [external_frame, 0], [external_frame, external_frame + self.height // 2], 'v', to_edge=door_step_ocean, symbol=x)

        center_sector = numpy.zeros((external_frame * 2 + self.height // 3, external_frame * 2 + self.width // 3), dtype='int32')
        center_sector_full = numpy.ones((self.height // 3, self.width // 3))
        center_sector[external_frame: external_frame + self.height // 3, external_frame: external_frame + self.width // 3] = center_sector_full
        line_dr.ant_line(center_sector, [external_frame, external_frame], [external_frame + self.width // 3, external_frame], 'g', to_edge=door_step_ocean, symbol=1)
        line_dr.ant_line(center_sector, [external_frame, external_frame], [external_frame, external_frame + self.height // 3], 'v', to_edge=door_step_ocean, symbol=1)
        line_dr.ant_line(center_sector, [external_frame, external_frame + self.height // 3], [external_frame + self.width // 3, external_frame + self.height // 3], 'g', to_edge=door_step_ocean, symbol=1, inverse=True)
        line_dr.ant_line(center_sector, [external_frame + self.width // 3, external_frame], [external_frame + self.width // 3, external_frame + self.height // 3], 'v', to_edge=door_step_ocean, symbol=1, inverse=True)

        beach_size = 6
        beach_door_step = 3
        beach_donut = numpy.ones((external_frame * 2 + self.height, external_frame * 2 + self.width), dtype='int32')
        beach_abyss = numpy.zeros((self.height - beach_size * 2, self.width - beach_size * 2), dtype='int32')
        beach_donut[external_frame + beach_size: external_frame + self.height - beach_size,
        external_frame + beach_size: external_frame + self.width - beach_size] = beach_abyss
        line_dr.ant_line(beach_donut, [external_frame + beach_size, external_frame + beach_size], [external_frame + self.width - beach_size, external_frame + beach_size], 'g', to_edge=beach_door_step, symbol=6, inverse=True)
        line_dr.ant_line(beach_donut, [external_frame + beach_size, external_frame + beach_size], [external_frame + beach_size, external_frame + self.height - beach_size], 'v',
                         to_edge=beach_door_step, symbol=6, inverse=True)
        line_dr.ant_line(beach_donut, [external_frame + self.width - beach_size, external_frame + beach_size], [external_frame + self.width - beach_size, external_frame + self.height - beach_size], 'v',
                         to_edge=beach_door_step, symbol=6, inverse=False)
        line_dr.ant_line(beach_donut, [external_frame + beach_size, external_frame + self.height - beach_size], [external_frame + self.width - beach_size, external_frame + self.height - beach_size], 'g',
                         to_edge=beach_door_step, symbol=6, inverse=False)

        for i in range(external_frame * 2 + self.height // 2):
            for j in range(external_frame * 2 + self.width // 2):
                position = world_layout[world_frame - external_frame + i][world_frame - external_frame + j]
                if position == 1 and lh_sector[i][j]:
                    world_layout[world_frame - external_frame + i][world_frame - external_frame + j] = lh_sector[i][j]

        for i in range(external_frame * 2 + self.height // 2):
            for j in range(external_frame * 2 + self.width // 2):
                position = world_layout[self.height // 2 + world_frame - external_frame + i][world_frame - external_frame + j]
                if position == 1 and ld_sector[i][j]:
                    world_layout[self.height // 2 + world_frame - external_frame + i][world_frame - external_frame + j] = ld_sector[i][j]

        for i in range(external_frame * 2 + self.height // 2):
            for j in range(external_frame * 2 + self.width // 2):
                position = world_layout[self.height // 2 + world_frame - external_frame + i][world_frame - external_frame + j + self.width // 2]
                if position == 1 and rd_sector[i][j]:
                    world_layout[self.height // 2 + world_frame - external_frame + i][world_frame - external_frame + j + self.width // 2] = rd_sector[i][j]

        for i in range(external_frame * 2 + self.height // 2):
            for j in range(external_frame * 2 + self.width // 2):
                position = world_layout[world_frame - external_frame + i][world_frame - external_frame + j + self.width // 2]
                if position in [1, one_x] and rh_sector[i][j]:
                    world_layout[world_frame - external_frame + i][world_frame - external_frame + j + self.width // 2] = rh_sector[i][j]

        for i in range(external_frame * 2 + self.height // 3):
            for j in range(external_frame * 2 + self.width // 3):
                position = world_layout[world_frame - external_frame + i + self.height // 3][world_frame - external_frame + j + self.width // 3]
                if position and center_sector[i][j]:
                    world_layout[world_frame - external_frame + i + self.height // 3][world_frame - external_frame + j + self.width // 3] = center_sector[i][j]

        for i in range(external_frame * 2 + self.height):
            for j in range(external_frame * 2 + self.width):
                position = world_layout[world_frame - external_frame + i][world_frame - external_frame + j]
                if beach_donut[i][j] and position:
                    world_layout[world_frame - external_frame + i][world_frame - external_frame + j] = 6
        self.world_layout = world_layout

    def create_world(self, external_frame=8):
        grass_variants = [pygame.image.load(f'textures\\grass_big_textures\\{image}').convert_alpha() for image in
                          os.listdir('textures\\grass_big_textures')]
        ground_variant = {}
        for image in os.listdir('textures\\ground'):
            ground_variant[int(image[0])] = pygame.image.load(f'textures\\ground\\{image}').convert_alpha()
        plot = self.world_layout.copy().tolist()
        grass_plot = self.world_layout.copy().tolist()
        for i_n, i_e in enumerate(self.world_layout):
            for j_n, j_e in enumerate(i_e):
                if j_e == 1:
                    grass_plot[i_n][j_n] = random.choice(grass_variants) if random.choice([True, False]) else False
                else:
                    grass_plot[i_n][j_n] = False
                plot[i_n][j_n] = ground_variant[j_e]
        self.world_layout = [plot, grass_plot]

    def make_player_coordinate(self, world_frame=10):
        from line_drawer import LineDrawer
        position = random.randint(0, self.width * 2 + self.height * 2)
        position_on_line = position % ((self.height + self.width) // 2)
        setup = [[1, position_on_line], [position_on_line, 1], [self.width + world_frame * 2 - 1, position_on_line],
                 [position_on_line, self.height + world_frame * 2 - 1]][position // ((self.height + self.width) // 2)]
        coordinates = LineDrawer.bresenham_line(setup[0], setup[1], self.width // 2 + world_frame,
                                                self.height // 2 + world_frame)
        for coordinate in coordinates:
            if self.world_layout[coordinate[0]][coordinate[1]] in [1, 2, 3, 4, 5, 6]:
                return coordinate
        return coordinates[0]

    def save_world_image(self, world_frame=10):
        ground_variant = {}
        for n, image in enumerate(os.listdir('textures\\ground')):
            ground_variant[n] = Image.open(f'textures\\ground\\{image}')
        image = Image.new("RGB", ((self.height + world_frame * 2) * 34, (self.width + world_frame * 2) * 54), (0, 0, 0))

        for n_1, i in enumerate(self.world_layout):
            for n_2, j in enumerate(i):
                image.paste(ground_variant[j], (n_1 * 34, n_2 * 54))
        image.save('Map_image.png')

    def return_world_layout(self):
        return self.world_layout


if __name__ == '__main__':
    a = WorldGenerator(100, 100)
    a.create_world_layout()
    a.save_world_image()

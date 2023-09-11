from PIL import Image
import numpy
import pygame
import random
import os


class WorldGenerator:
    def __init__(self, height, width, sector_size=256):
        self.height = height
        self.width = width
        self.sector_size = sector_size
        self.world_layout = []

    def create_world_layout(self, world_frame=10):
        from line_drawer import LineDrawer
        door_step_ocean = 5
        world_layout = numpy.zeros((world_frame * 2 + self.height, world_frame * 2 + self.width), dtype='int32')
        island_layout = numpy.ones((self.height, self.width), dtype='int32')
        sign = -1
        island_layout_1 = numpy.array([[sign for _ in range(self.width)] for _ in range(self.height)])
        world_layout[world_frame: world_frame + self.height, world_frame: world_frame + self.width] = island_layout
        line_dr = LineDrawer()
        line_dr.ant_line(world_layout, [world_frame, world_frame], [world_frame + self.width, world_frame], 'g', door_step=door_step_ocean)
        line_dr.ant_line(world_layout, [world_frame + self.width, world_frame], [world_frame + self.width, world_frame + self.height], 'v', inverse=True, door_step=door_step_ocean)
        line_dr.ant_line(world_layout, [world_frame, world_frame + self.height], [world_frame + self.width, world_frame + self.height], 'g', inverse=True, door_step=door_step_ocean)
        line_dr.ant_line(world_layout, [world_frame, world_frame], [world_frame, world_frame + self.height], 'v', door_step=door_step_ocean)

        external_frame = 8
        regions = [2, 3, 4, 5]
        one_x = 0
        lh_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2), dtype='int32')
        x = random.choice(regions)
        one_x = x
        regions.remove(x)
        lh_sector_full = numpy.array([[x for _ in range(external_frame * 2 + self.width // 2)] for _ in range(external_frame + self.height // 2)])
        lh_sector[0: external_frame + self.height // 2, 0: external_frame * 2 + self.width // 2] = lh_sector_full
        line_dr.ant_line(lh_sector, [0, external_frame + self.height // 2], [external_frame * 2 + self.width // 2, external_frame + self.height // 2], 'g', door_step=door_step_ocean, sign=x, inverse=True)

        ld_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2), dtype='int32')
        x = random.choice(regions)
        regions.remove(x)
        ld_sector_full = numpy.array([[x for _ in range(external_frame + self.width // 2)] for _ in range(external_frame * 2 + self.height // 2)])
        ld_sector[0: external_frame * 2 + self.height // 2, 0: external_frame + self.width // 2] = ld_sector_full
        line_dr.ant_line(ld_sector, [external_frame + self.width // 2, 0], [external_frame + self.width // 2, external_frame * 2 + self.height // 2], 'v', door_step=door_step_ocean, sign=x, inverse=True)

        rd_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2), dtype='int32')
        x = random.choice(regions)
        regions.remove(x)
        rd_sector_full = numpy.array([[x for _ in range(external_frame * 2 + self.width // 2)] for _ in range(external_frame + self.height // 2)])
        rd_sector[external_frame: external_frame * 2 + self.height // 2, 0: external_frame * 2 + self.width // 2] = rd_sector_full
        line_dr.ant_line(rd_sector, [0, external_frame], [external_frame + self.width // 2, external_frame], 'g', door_step=door_step_ocean, sign=x)

        rh_sector = numpy.zeros((external_frame * 2 + self.height // 2, external_frame * 2 + self.width // 2), dtype='int32')
        x = random.choice(regions)
        regions.remove(x)
        rh_sector_full = numpy.array([[x for _ in range(external_frame + self.width // 2)] for _ in range(external_frame * 2 + self.height // 2)])
        rh_sector[0: external_frame * 2 + self.height // 2, external_frame: external_frame * 2 + self.width // 2] = rh_sector_full
        line_dr.ant_line(rh_sector, [external_frame, 0], [external_frame, external_frame + self.height // 2], 'v', door_step=door_step_ocean, sign=x)

        # center_sector = numpy.zeros((external_frame * 2 + self.height // 4, external_frame * 2 + self.width // 4), dtype='int32')
        # [print(i) for i in center_sector]
        # center_sector_full = numpy.ones((self.height // 4, self.width // 4))
        # center_sector[external_frame: external_frame + self.height // 4, external_frame: external_frame + self.width // 4] = center_sector_full
        # line_dr.ant_line(center_sector, [external_frame, external_frame], [external_frame, external_frame + self.height // 4], 'g', door_step=door_step_ocean, sign=1)
        # line_dr.ant_line(center_sector, [external_frame, external_frame], [external_frame + self.width // 4, external_frame], 'v', door_step=door_step_ocean, sign=1)
        # line_dr.ant_line(center_sector, [external_frame + self.width // 4, external_frame], [external_frame + self.width // 4, external_frame + self.height // 4], 'g', door_step=door_step_ocean, sign=1, inverse=True)
        # line_dr.ant_line(center_sector, [external_frame, external_frame + self.height // 4], [external_frame + self.width // 4, external_frame + self.height // 4], 'v', door_step=door_step_ocean, sign=1, inverse=True)


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

        # for i in range(external_frame * 2 + self.height // 3):
        #     for j in range(external_frame * 2 + self.width // 3):
        #         position = world_layout[world_frame - external_frame + i + self.height // 3][world_frame - external_frame + j + self.width // 3]
        #         if position and center_sector[i][j]:
        #             world_layout[world_frame - external_frame + i + self.height // 3][world_frame - external_frame + j + self.width // 3] = center_sector[i][j]

        self.world_layout = world_layout



    def create_world(self):
        grass_variants = [pygame.image.load(f'textures\\grass\\{image}').convert_alpha() for image in os.listdir('textures\\grass')]
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

    def create_regions(self):
        pass

    def save_world_image(self, world_frame=10):
        ground_variant = {}
        for n, image in enumerate(os.listdir('textures\\ground')):
            ground_variant[n] = Image.open(f'textures\\ground\\{image}')
        image = Image.new("RGB", ((self.height + world_frame * 2) * (154 - 28), (self.width + world_frame * 2) * (128 - 23)), (0, 0, 0))
        for n_1, i in enumerate(self.world_layout):
            for n_2, j in enumerate(i):
                image.paste(ground_variant[j], (n_1 * (154 - 28), n_2 * (128 - 23)))
        image.save('Map_image.png')

    def return_world_layout(self):
        return self.world_layout

if __name__ == '__main__':
    a = WorldGenerator(100, 100)
    a.create_world_layout()
    a.save_world_image()
from PIL import Image, ImageDraw
# import numpy
import pygame
import random
import os


class WorldGenerator:
    def __init__(self, height, width, sector_size=256):
        self.height = height
        self.width = width
        self.sector_size = sector_size
        self.world_layout = []

    def while_generate(self):
        self.world_layout = [[(i + j, i * j, i - j) for j in range(self.width)] for i in range(self.height)]

    def create_test_world(self):
        grass = [pygame.image.load(f'textures\\grass\\{image}').convert_alpha() for image in os.listdir('textures\\grass')]
        ground = pygame.image.load('textures\\ground\\var. 1 xl.png').convert_alpha()
        plot = [[ground for j in range(100)] for i in range(100)]
        grass = [[random.choice(grass) if random.choice([True, False]) else False for j in range(100)] for i in range(100)]
        self.world_layout = [plot, grass]

    # def create_test_world_2(self):




    def save_world_image(self, version):
        # version 1
        if version == 1:
            image = Image.new("RGB", (self.height, self.width), (0, 0, 0))
            pixels = image.load()
            for i in range(self.height):
                for j in range(self.width):
                    pixels[i, j] = self.world_layout[i][j]
            image.save('Map_image.bmp')

        # version 2
        elif version == 2:
            image = Image.new("RGB", (self.height * self.sector_size, self.width * self.sector_size), (0, 0, 0))
            desk = ImageDraw.Draw(image)
            for i in range(self.height):
                for j in range(self.width):
                    desk.rectangle((self.sector_size * j, self.sector_size * i, self.sector_size * (j + 1) - 1, self.sector_size * (i + 1) - 1), fill=self.world_layout[i][j])
            image.save('Map_image_1.bmp')

    def return_world_layout(self):
        return self.world_layout

    def test_auto_action(self, n_1=2):
        # self.while_generate()
        self.create_test_world()
        # self.save_world_image(n_1)
        return self.return_world_layout()


if __name__ == '__main__':
    draw = WorldGenerator(100, 100, sector_size=8)
    draw.while_generate()
    draw.save_world_image(2)

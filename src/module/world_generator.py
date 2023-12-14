from typing import List

import numpy

from pygame.image import load
from pygame.surface import Surface


class WorldGenerator:
    def __init__(self):
        self.world: numpy.ndarray = numpy.array([])
        self.textures = {1: 'grass_place', 2: 'sand_place'}
        self.set_textures()

    def set_textures(self) -> None:
        texture_name = self.textures
        self.textures = {}
        for name in texture_name:
            self.textures[name] = load(f"../../data/textures/world/{texture_name[name]}.png").convert_alpha()

    def texturing_process(self, world_element):
        return self.textures[world_element]

    def texturing(self, world) -> numpy.ndarray:
        return numpy.vectorize(self.texturing_process)(world)

    def test_create_world(self) -> None:
        grass_list = numpy.full(shape=(100, 100), fill_value=1)
        sand_list = numpy.full(shape=(100, 100), fill_value=2)
        # self.world = self.texturing(numpy.array([grass_list, sand_list]))
        self.world = numpy.array([grass_list, sand_list]).tolist()

    def get_world(self) -> numpy.ndarray:
        return self.world

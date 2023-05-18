import map_generation
import pygame
import random

class MapDrawer:
    def __init__(self, map_size, sector_size, quantity_of_points):
        self.map_size = map_size
        self.sector_size = sector_size
        self.quantity_of_points = quantity_of_points
        self.game_map = list()
        self.dictionary_of_colors_map = {}

    def map_generate(self):
        self.game_map = map_generation.MapGeneration(self.map_size[0], self.map_size[1], self.quantity_of_points).main()

    def color_generate(self):
        for line in self.game_map:
            for number in line:
                if number not in self.dictionary_of_colors_map:
                    self.dictionary_of_colors_map[number] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def draw_game_map(self, game_screen, player_position, camera_position, fill=0):
        def color_correct(color, fill):
            if not fill:
                return color
            return tuple([meaning + fill if meaning + fill <= 255 else 255 for meaning in color])
        game_screen.fill((255, 255, 255))
        x = 0
        y = 0
        for row in self.game_map:
            for col in row:
                pygame.draw.rect(game_screen, color_correct(self.dictionary_of_colors_map[col], fill), (x - player_position[0] + camera_position[0], y - player_position[1] + camera_position[1], self.sector_size[0], self.sector_size[1]))
                x += self.sector_size[0]
            y += self.sector_size[1]
            x = 0

    def combine_dictionaries(self, other_dict):
        for color in self.dictionary_of_colors_map:
            other_dict[color] = self.dictionary_of_colors_map[color]

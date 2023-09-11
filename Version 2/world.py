import pygame
from numpy import array


class World:
    def __init__(self, screen, sector_scale, world_layout, player_coordinate):
        self.world_layout = world_layout
        self.player_coordinate = player_coordinate
        self.player_position = []
        self.screen = screen
        self.sector_scale = [sector_scale[0] - 26, sector_scale[1] - 24]

    # Хрень
    # def get_world_section(self, x_1, x_2, y_1, y_2):
    #     return [layer[y_1: y_2, x_1: x_2].tolist() for layer in self.world_layout]

    def set_player_coordinate(self, player_coordinate):
        self.player_coordinate = player_coordinate

    def calculate_player_position(self):
        self.player_position = [self.player_coordinate[0] // self.sector_scale[0], self.player_coordinate[1] // self.sector_scale[1]]

    def draw_world(self, frame_rate):
        self.screen.fill('white')
        self.calculate_player_position()
        x = self.player_position[0] * self.sector_scale[0]
        y = self.player_position[1] * self.sector_scale[1]
        for i in range(self.player_position[1] - 7, self.player_position[1] + 7):
            for j in range(self.player_position[0] - 9, self.player_position[0] + 9):
                for layer in range(len(self.world_layout)):
                    if 0 <= i < len(self.world_layout[layer]) and 0 <= j < len(self.world_layout[layer][0]):
                        if self.world_layout[layer][j][i]:
                            try:
                                self.screen.blit(self.world_layout[layer][j][i], (x - self.player_coordinate[0], y - self.player_coordinate[1]))
                            except:
                                print(self.world_layout)
                                exit()
                x += self.sector_scale[0]
            y += self.sector_scale[1]
            x = self.player_position[0] * self.sector_scale[0]

from textures_reader import TexturesReader

"""
Класс объекта персонаж, который хранит в себе значения и передаёт их, рисует персонажа
"""


class Player:
    def __init__(self, screen, fps, position):
        self.fps = fps
        self.regularity = 5
        # self.every_frame = [[(frame + 1) * self.regularity for frame in range(self.fps // self.regularity)], 0]  # var 1
        self.every_frame = [[(frame + 1) * (self.fps // self.regularity) for frame in range(self.regularity)], 0]  # var 2
        self.position = position  # [x, y]
        self.screen = screen
        self.player_motion_step = 27 if self.fps == 30 else 13
        self.player_textures = TexturesReader('textures\\player\\Ashmed').get_textures('player')
        self.player_sprite_size = self.player_textures['up'][0].get_size()
        self.player_sprite_size = [34, 54]
        self.player_side = 'down'  # up, down, left, right
        self.status = 'worth'  # run, worth

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def change_position(self, axis, position, action):
        number = {'x': 0, 'y': 1}[axis]
        action = {'+': lambda a, b: a + b, '-': lambda a, b: a - b, '=': lambda a, b: b}[action]
        self.position[number] = action(self.position[number], position)

    def calculate_texture(self, frame_rate):
        texture = None
        if self.status == 'worth':
            texture = self.player_textures[self.player_side][0]
        elif self.status == 'run':
            texture = self.player_textures[self.player_side][self.every_frame[1]]
            if frame_rate in self.every_frame[0]:
                self.every_frame[1] = (self.every_frame[1] + 1) % 4
        return texture

    def draw_player(self, frame_rate):
        self.screen.blit(self.calculate_texture(frame_rate),
                         (960 - self.player_sprite_size[0] // 2, 540 - self.player_sprite_size[1] // 2))

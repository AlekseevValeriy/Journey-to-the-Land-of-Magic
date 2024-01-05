from random import choice, randint, choices

import pygame

from player import Player
from os import listdir
from pygame.image import load


class Enemies:
    def __init__(self, screen, world_map, fps=30, world_sector_size=100, enemy_limit=1):
        self.screen = screen
        self.world_map = world_map[0]
        self.fps = fps
        self.world_sector_size = world_sector_size
        self.world_size = (len(self.world_map), len(self.world_map[0]))
        self.back_frame = (10, 10)
        self.enemies_stack = []
        self.enemy_limit = enemy_limit - 1

    def create_enemy(self, player_position: tuple):
        player_sectors_position = (
            player_position[0] // self.world_sector_size, player_position[1] // self.world_sector_size)
        end_1 = player_sectors_position[0] - self.back_frame[0]
        start_1 = player_sectors_position[0] + self.back_frame[0]
        x_pos = (*tuple(range(0, end_1 if end_1 >= 0 else 0)),
                 *tuple(range(start_1 if start_1 <= self.world_size[0] - 1 else self.world_size[0] - 1,
                              self.world_size[0] - 1)))
        end_2 = player_sectors_position[1] - self.back_frame[1]
        start_2 = player_sectors_position[1] + self.back_frame[1]
        y_pos = (*tuple(range(0, end_2 if end_2 >= 0 else 0)),
                 *tuple(range(start_2 if start_2 <= self.world_size[1] - 1 else self.world_size[1] - 1,
                              self.world_size[1] - 1)))

        position = (choice(x_pos), choice(y_pos))
        position = tuple(0 if i < 0 else i if 0 <= i < self.world_size[n] else self.world_size[n] - 1 for n, i in
                         enumerate(position))
        position_sector = self.world_map[position[1]][position[0]]

        if position_sector == 1:
            enemies_list = [TestEnemy]
        elif position_sector == 2:
            enemies_list = [TestEnemy]
        enemy_class = choice(enemies_list)
        enemy = enemy_class(self.screen, tuple(i * self.world_sector_size for i in position), 'test_enemy',
                            fps=self.fps)
        self.enemies_stack.append(enemy)

    def can_create(self) -> bool:
        if len(self.enemies_stack) <= self.enemy_limit:
            return True
        return False

    def draw_enemies(self, player_position):
        for enemy in self.enemies_stack:
            enemy.draw_player(player_position)

    def move_enemies(self):
        for enemy in self.enemies_stack:
            enemy.move()

    def get_positions(self):
        return tuple(map(lambda enemy: enemy.get_position(), self.enemies_stack))

    def get_rects(self):
        return tuple(map(lambda enemy: (*enemy.get_position(), *enemy.get_p_size()), self.enemies_stack))

    def is_together(self, player_pos_siz: tuple[int, int, int, int]):
        player_rect = pygame.Rect(player_pos_siz)
        together = tuple(map(player_rect.colliderect, self.get_rects()))
        if any(together):
            return self.enemies_stack[together.index(True)]
        return False

    def __delitem__(self, key):
        del self.enemies_stack[self.enemies_stack.index(key)]


class Enemy(Player):
    def __init__(self, screen, position, person, **personal_data):
        super().__init__(screen=screen, position=position, person=None, **personal_data)
        self.step_on_30_frame_rate = 10
        self.move_status = 'run'
        self.face_side = 'left'
        self.change_animation_under_fps(personal_data['fps'])
        self.action_counter = 0
        self.actions_dict = {15: 'up', 30: 'right', 45: 'down', 60: 'left'}
        self.set_size((34, 50))

    def set_textures(self):
        for image in listdir(f"../../data/textures/enemies/{self.person}"):
            self.textures[image.removesuffix('.png')] = load('/'.join([f"../../data/textures/enemies/{self.person}",
                                                                       image])).convert_alpha()

    def move(self):

        self.action_counter += 1
        if self.action_counter in self.actions_dict:
            self.face_side = self.actions_dict[self.action_counter]

        if self.action_counter >= 60:
            self.action_counter = 0
        self.sample_move('run')

    def get_rect(self):
        return (*self.position, *self.get_p_size())

    def draw_player(self, player_position):
        self.texture_selection()
        texture = self.textures.get(self.present_texture, self.textures['up_run_0'])
        self.screen.blit(texture, tuple(i - j for i, j in zip(self.position, player_position)))

    def battle_preparing(self):
        return {'texture': self.textures['left_run_0'], "side": 'right'}


class TestEnemy(Enemy):
    def __init__(self, screen, position, person, **personal_data):
        super().__init__(screen=screen, position=position, person=None, **personal_data)
        self.person = person
        self.set_textures()

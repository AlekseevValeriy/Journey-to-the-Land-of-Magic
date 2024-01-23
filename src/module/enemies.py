from os import listdir
from random import choice, randint

import pygame
from pygame.image import load

from player import Player


class Enemies:
    '''Класс врагов'''

    def __init__(self, screen: pygame.Surface, world_map: list, fps=30, world_sector_size=100, enemy_limit=1) -> None:
        self.screen = screen
        self.world_map = world_map[0]
        self.fps = fps
        self.world_sector_size = world_sector_size
        self.world_size = (len(self.world_map), len(self.world_map[0]))
        self.back_frame = (10, 10)
        self.enemies_stack = []
        self.enemy_limit = enemy_limit - 1

    def create_enemy(self, player_position: tuple) -> None:
        '''Метод создания врагов'''
        position = (randint(0, self.world_size[0] - 1), randint(0, self.world_size[1] - 1))
        if len(self.world_map) > 3:
            position_sector = self.world_map[position[1]][position[0]]
        else:
            position_sector = self.world_map[0][position[1]][position[0]]
        enemies_list = []
        if position_sector == 0:
            pass
        elif position_sector == 1:
            enemies_list = [ShroomishEnemy]  # лес - гусеница, растение
        elif position_sector == 2:
            enemies_list = [TorchikEnemy]  # пустыня - червяк, коршун
        elif position_sector == 3:
            enemies_list = [PachirisuEnemy]  # ледяная пустыня - белый медведь, тюлень
        elif position_sector == 4:
            enemies_list = [TestEnemy]  # багрянец - паук, зомби
        elif position_sector == 5:
            enemies_list = [TestEnemy]  # болото - динозавр, травяной монстр
        elif position_sector == 6:
            pass  # пляж - ничего

        if enemies_list:
            enemy_class = choice(enemies_list)
            enemy = enemy_class(self.screen, tuple(i * self.world_sector_size for i in position),
                                fps=self.fps)
            self.enemies_stack.append(enemy)

    def can_create(self) -> bool:
        '''Метод проверки возможности на создание врагов'''
        if len(self.enemies_stack) <= self.enemy_limit:
            return True
        return False

    def draw_enemies(self, player_position: tuple) -> None:
        '''Метод отрисовки врагов'''
        for enemy in self.enemies_stack:
            enemy.draw_player(player_position)

    def move_enemies(self) -> None:
        '''Метод движения врагов'''
        for enemy in self.enemies_stack:
            enemy.move()

    def get_positions(self) -> tuple:
        '''Метод получения позиций врагов'''
        return tuple(map(lambda enemy: enemy.get_position(), self.enemies_stack))

    def get_rects(self) -> tuple:
        '''Метод получение хит боксов врагов'''
        return tuple(map(lambda enemy: (*enemy.get_position(), *enemy.get_p_size()), self.enemies_stack))

    def is_together(self, player_pos_siz: tuple[int, int, int, int]) -> bool:
        player_rect = pygame.Rect(player_pos_siz)
        together = tuple(map(player_rect.colliderect, self.get_rects()))
        if any(together):
            return self.enemies_stack[together.index(True)]
        return False

    def __delitem__(self, key):
        del self.enemies_stack[self.enemies_stack.index(key)]

    def clear(self) -> None:
        '''Метод очистки стака врагов'''
        self.enemies_stack = []

    def set_world(self, world: list) -> None:
        '''Метод установки мира'''
        self.world_map = world
        self.world_size = (len(self.world_map), len(self.world_map[0]))


class Enemy(Player):
    '''Класс Врага'''

    def __init__(self, screen: pygame.Surface, position: tuple, person: str, **personal_data) -> None:
        super().__init__(screen=screen, position=position, person=None, **personal_data)
        self.step_on_30_frame_rate = 10
        self.move_status = 'run'
        self.face_side = 'left'
        self.change_animation_under_fps(personal_data['fps'])
        self.action_counter = 0
        self.actions_dict = {15: 'up', 30: 'right', 45: 'down', 60: 'left'}
        self.set_size((34, 50))

    def set_textures(self) -> None:
        '''Метод установки текстур'''
        for image in listdir(f"../../data/textures/enemies/{self.person}"):
            self.textures[image.removesuffix('.png')] = load(
                '/'.join([f"../../data/textures/enemies/{self.person}", image])).convert_alpha()

    def move(self) -> None:
        '''Метод движения врага'''
        self.action_counter += 1
        if self.action_counter in self.actions_dict:
            self.face_side = self.actions_dict[self.action_counter]

        if self.action_counter >= 60:
            self.action_counter = 0
        self.sample_move('run')

    def get_rect(self) -> tuple:
        '''Метод получения хит бокса'''
        return *self.position, *self.get_p_size()

    def draw_player(self, player_position: tuple) -> None:
        '''Метод отрисовки врага'''
        self.texture_selection()
        texture = self.textures.get(self.present_texture, self.textures['up_run_0'])
        self.screen.blit(texture, tuple(i - j for i, j in zip(self.position, player_position)))

    def battle_preparing(self) -> dict:
        '''Метод подготовки к битве'''
        return {'texture': self.textures['left_run_0'], "side": 'right'}


class TestEnemy(Enemy):
    '''Класс тестового врага'''

    def __init__(self, screen: pygame.Surface, position: tuple, person: str='test_enemy', **personal_data) -> None:
        super().__init__(screen=screen, position=position, person=None, **personal_data)
        self.person = person
        self.set_textures()

class TorchikEnemy(Enemy):
    '''Класс врага Торчик'''

    def __init__(self, screen: pygame.Surface, position: tuple, person: str='torchik', **personal_data) -> None:
        super().__init__(screen=screen, position=position, person=None, **personal_data)
        self.person = person
        self.set_textures()

class PachirisuEnemy(Enemy):
    '''Класс врага Пачирису'''

    def __init__(self, screen: pygame.Surface, position: tuple, person: str='pachirisu', **personal_data) -> None:
        super().__init__(screen=screen, position=position, person=None, **personal_data)
        self.person = person
        self.set_textures()

class ShroomishEnemy(Enemy):
    '''Класс врага Шрумиш'''
    def __init__(self, screen: pygame.Surface, position: tuple, person: str='shroomish', **personal_data) -> None:
        super().__init__(screen=screen, position=position, person=None, **personal_data)
        self.person = person
        self.set_textures()

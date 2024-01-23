import random
from random import choices
from sys import exit
from typing import Callable

import pygame.image
from pygame import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, KEYDOWN, KEYUP, K_x, K_u, K_m, K_i, K_s, K_ESCAPE, \
    K_p, K_r, K_e, K_t, K_q, Surface, K_g
from pygame.display import update
from pygame.event import get
from pygame.time import Clock

from battle import Battle
from buttons_menu import ButtonsMenu
from collision import Collision
from custom_object_buttons import StatusBar, WorldMap, SkillUpgrade, MagicUpgrade, BigMap
from enemies import Enemies
from json_reader import JsonReader
from music_manager import MusicManager
from player import Player
from world import World
from world_generator import WorldGenerator


class GameButtonsMenu(ButtonsMenu):
    '''Класс игрового меню'''

    def __init__(self, screen: Surface, clock: Clock, frame_rate: int, buttons_file_path: str, sample_world=None,
                 player_data=None, world_number=None):
        super().__init__(screen=screen, clock=clock, frame_rate=frame_rate, buttons_file_path=buttons_file_path)
        self.add_other_data(move=False,
                            background=pygame.image.load('../../data/textures/backgrounds/background.png').convert(),
                            pressed_mouse_map=False, fps_counter=True,
                            fps_font=pygame.font.SysFont('Comic Sans MS', 30), music_manager=MusicManager(0.5),
                            generator=WorldGenerator(), in_door=False, god=False)
        self.add_button_bind(back_button=self.end_menu, person_menu_enter_button=self.to_person_menu,
                             map_menu_enter_button=self.to_map_menu, back_to_game=self.to_game_menu,
                             to_upgrade_characteristics=self.to_upgrade_characteristics,
                             to_upgrade_magic=self.to_upgrade_magic, add_str=self.add_str_point,
                             add_dex=self.add_dex_point, add_int=self.add_int_point, add_fb=self.add_fb)
        self.keys_dict = {1073741903: 'right', 1073741904: 'left', 1073741906: 'up', 1073741905: 'down'}
        self.world = None
        self.player = None
        self.doors = None
        self.sample_world = sample_world
        self.player_data = player_data
        self.world_number = world_number
        self.battle_thing = Battle(self.screen, self.clock, self.frame_rate, '../../data/json/battle_buttons.json')
        self.create_button_objects()
        self.collision = Collision()
        self.number = -1
        self.door_layout = None

    def click_sound(function: Callable):
        '''Декоратор звука нажатия'''

        def click(self, *args, **kwargs):
            function(self, *args, **kwargs)
            self.other_data['music_manager'].activate_effect('click')

        return click

    def add_collision_blocks(self, world: list) -> None:
        '''Метод добавления коллизии'''
        world_sector = (100, 100)
        for n, y in enumerate(world):
            for m, x in enumerate(y):
                if x == 0:
                    self.collision.add_block(position=(m * world_sector[0], n * world_sector[1]),
                                             sprite_size=world_sector)

    def create_button_objects(self) -> None:
        '''Метод создания объектов'''
        objects_sb = self.objects_data['game_menu']['sb']
        self.objects_data['game_menu']['sb'] = StatusBar(self.screen,
                                                         *tuple(map(lambda name: objects_sb[name], objects_sb)))
        objects_mp = self.objects_data['game_menu']['mp']
        self.objects_data['game_menu']['mp'] = WorldMap(self.screen,
                                                        *tuple(map(lambda name: objects_mp[name], objects_mp)))
        objects_cu = self.objects_data['characteristic_menu']['cu']
        self.objects_data['characteristic_menu']['cu'] = SkillUpgrade(self.screen, *tuple(
            map(lambda name: objects_cu[name], objects_cu)))

        objects_mu = self.objects_data['magic_menu']['mu']
        self.objects_data['magic_menu']['mu'] = MagicUpgrade(self.screen,
                                                             *tuple(map(lambda name: objects_mu[name], objects_mu)))

        self.objects_data['map_menu'] = {}
        self.objects_data['map_menu']['bmp'] = BigMap(self.screen)

    def create_world(self, world: list) -> None:
        '''Метод создания мира'''
        self.world = World(self.screen, world)

    def create_player(self, person: str, position: tuple) -> None:
        '''Метод создания игрока'''
        self.player = Player(self.screen, position, person)
        self.player.set_size((34, 50))

        self.objects_data['game_menu']['sb'].born()

    def start_menu(self, frame_rate: int) -> None:
        '''Метод старта игрового процесса'''
        self.frame_rate = frame_rate
        self.objects_data['game_menu']['mp'].set_world_map(self.sample_world)
        self.objects_data['game_menu']['mp'].set_frame(self.player.get_frame())
        self.objects_data['game_menu']['mp'].set_player_position(self.player.get_position())
        self.objects_data['map_menu']['bmp'].data['world_map'] = (
            self.objects_data['game_menu']['mp'].data['world_map'])
        self.objects_data['map_menu']['bmp'].data['world_size'] = self.objects_data['game_menu']['mp'].data[
            'world_size']
        self.player.change_animation_under_fps(self.frame_rate)
        self.objects_data['game_menu']['sb'].add_data(**self.player_data)
        self.objects_data['characteristic_menu']['cu'].add_data(
            **self.objects_data['game_menu']['sb'].get_characteristics())
        self.objects_data['characteristic_menu']['cu'].add_data(
            **self.objects_data['game_menu']['sb'].get_characteristics())
        self.objects_data['characteristic_menu']['cu'].update_points()
        self.objects_data['magic_menu']['mu'].add_data(**self.objects_data['game_menu']['sb'].get_magic_data())
        self.objects_data['magic_menu']['mu'].update_points()
        self.enemies_generator = Enemies(self.screen, self.sample_world, enemy_limit=20)
        value = (JsonReader.read_file('../../data/json/settings_data.json')['volume_trigger_position'] - 816) * 100 // (
                1100 - 816) / 100
        if value > 1:
            value = 1
        if value < 0:
            value = 0
        self.other_data['music_manager'].set_volume(value)
        self.other_data['music_manager'].activate_music('middle_piano')

        self.add_collision_blocks(self.sample_world[0])
        self.collision.set_player_sprite(self.player.get_position(), (10, 20))

        self.menu_process_flag = True
        self.present_menu = 'game_menu'
        self.menu_process()

    def menu_process(self) -> None:
        '''Метод игрового меню'''
        while self.menu_process_flag:
            if self.present_menu == 'game_menu':
                self.game_unit()
                self.objects_data['game_menu']['sb'].dead_check()
                self.enemies_generator.draw_enemies(self.player.get_position())
                self.enemies_generator.move_enemies()
                self.start_battle(
                    self.enemies_generator.is_together((*self.player.get_position_sp(), *self.player.get_p_size())))
            else:
                self.draw_background()

            self.draw_buttons(self.present_menu)
            self.draw_objects(self.present_menu)
            self.cursor_reader()
            self.draw_fps()

            if self.menu_process_flag:
                update()
                self.clock.tick(self.frame_rate)

    def draw_background(self) -> None:
        '''Метод отрисовки заднего фона'''
        self.screen.blit(self.other_data['background'], (0, 0))

    def game_unit(self) -> None:
        '''Метод отрисовки вещей во время нахождения в мире'''
        self.screen.fill('white')
        self.world.draw_world(self.player.get_position())
        self.player.draw_player()

    def draw_fps(self) -> None:
        '''Метод отрисовки счётчика fps'''
        if self.other_data['fps_counter']:
            text = self.other_data['fps_font'].render(str(int(self.clock.get_fps())), True, 'gray')
            self.screen.blit(text, (1879, 5))

    def cursor_reader(self) -> None:
        '''Метод обработки действий'''
        for event in get():
            if event.type == QUIT:
                self.menu_process_flag = False
                exit()
            if self.present_menu == 'game_menu':
                if event.type == KEYDOWN and self.objects_data['game_menu']['sb'].get_persona_status():
                    if self.keys_dict.get(event.key, False):
                        self.objects_data['game_menu']['mp'].set_frame(self.player.get_frame())
                        self.objects_data['game_menu']['mp'].set_player_position(self.player.get_position())
                        self.run_action(self.keys_dict[event.key])
                    if event.key == K_x:
                        self.objects_data['game_menu']['sb'].reduce_parameter('hp', 10)
                    if event.key == K_u:
                        self.objects_data['characteristic_menu']['cu'].data['free_points'] += 1
                        self.objects_data['characteristic_menu']['cu'].update_points()
                        self.objects_data['game_menu']['sb'].data['magic_free_points'] += 1
                    if event.key == K_i:
                        self.objects_data['magic_menu']['mu'].data['free_points'] += 1
                        self.objects_data['magic_menu']['mu'].update_points()
                        self.objects_data['game_menu']['sb'].data['free_points'] += 1
                    if event.key == K_m:
                        self.to_map_menu()
                    if event.key == K_g:
                        self.other_data['god'] = True
                    if event.key == K_s:
                        self.player.step_on_30_frame_rate = 54
                        self.player.change_animation_under_fps(self.frame_rate)
                    if event.key == K_ESCAPE:
                        if self.present_menu == 'game_menu':
                            self.end_menu()
                    if event.key == K_p:
                        self.present_menu = 'persons_menu'
                    if event.key in (K_r, K_e, K_t):
                        position = self.player.get_position_sp()
                        position = position[0] // 100, position[1] // 100
                        if event.key == K_r:
                            if self.sample_world[2][position[1]][position[0]] == 13:
                                if all(self.objects_data['game_menu']['sb'].get_chips()):
                                    self.game_end()
                        elif event.key == K_e:
                            if self.sample_world[2][position[1]][position[0]] == 12:
                                self.enter_in_door(str(position[0]) + str(position[1]))
                        elif event.key == K_t:
                            if self.door_layout != None:
                                data = JsonReader.read_file('../../data/json/units_data.json')
                                door = data[f'unit_{self.world_number}']['doors'][self.number]
                                if self.door_layout != None:
                                    if door[1][position[1]][position[0]] == 20:
                                        if self.number != -1:
                                            door[1][position[1]][position[0]] = -1
                                            data[f'unit_{self.world_number}']['doors'][self.number] = door
                                            JsonReader.write_file(data, '../../data/json/units_data.json')

                                            self.objects_data['game_menu']['mp'].set_world_map(
                                                JsonReader.read_file('../../data/json/units_data.json')[
                                                    f'unit_{self.world_number}']['doors'][self.number])
                                            self.objects_data['map_menu']['bmp'].data['world_map'] = (
                                                self.objects_data['game_menu']['mp'].data['world_map'])
                                            self.objects_data['map_menu']['bmp'].data['world_size'] = \
                                                self.objects_data['game_menu']['mp'].data['world_size']

                                            self.world.set_world(self.other_data['generator'].texturing(door))

                                            self.add_chip()
                    if event.key == K_q:
                        if self.door_layout != None:
                            self.enter_in_world()

                elif event.type == KEYUP:
                    if event.key == K_s:
                        self.player.step_on_30_frame_rate = 12
                        self.player.change_animation_under_fps(self.frame_rate)
                    if event.key == K_g:
                        self.other_data['god'] = False
                    if self.keys_dict.get(event.key, False) or not self.objects_data['game_menu'][
                        'sb'].get_persona_status():
                        self.player.clear_frame_skip()
                        self.stand_action()
                if self.enemies_generator.can_create():
                    if choices([0, 1], weights=(0, 1)):
                        self.enemies_generator.create_enemy(self.player.get_position())
            if self.present_menu == 'map_menu':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.objects_data['map_menu']['bmp'].change_sector_size(0.2)
                    elif event.button == 5:
                        self.objects_data['map_menu']['bmp'].change_sector_size(-0.2)

                    if self.objects_data['map_menu']['bmp'].in_map(event.pos):
                        self.other_data['pressed_mouse_map'] = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.other_data['pressed_mouse_map'] = False
                if event.type == pygame.MOUSEMOTION:
                    if self.other_data['pressed_mouse_map']:
                        self.objects_data['map_menu']['bmp'].position_move(event.rel)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.present_menu = 'game_menu'
            if self.present_menu == 'persons_menu':
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.present_menu = 'game_menu'
            if self.present_menu in ['characteristic_menu', 'magic_menu']:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.present_menu = 'persons_menu'
            if event.type == MOUSEMOTION:
                buttons = self.buttons_data[self.present_menu]
                for button in buttons:
                    if event.pos in buttons[button] and not buttons[button].status == 'unactive':
                        buttons[button].status = 'active'
                    else:
                        if buttons[button].status == 'active':
                            buttons[button].status = 'passive'
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons = self.buttons_data[self.present_menu]
                    for button in buttons:
                        if event.pos in buttons[button]:
                            self.buttons_binds.get(button, self.not_found_function)()
            elif event.type == MOUSEBUTTONUP:
                pass

        if self.other_data['move']:
            if not self.other_data['god']:
                if self.collision.co_co_in(self.player.fake_move()):
                    pass
                else:
                    self.player.player_move('run')
            else:
                self.player.player_move('run')
        else:
            self.player.player_move('stand')

    def add_chip(self) -> None:
        '''Метод добавления осколка'''
        chips = (
            self.objects_data['game_menu']['sb'].data['chip_1'], self.objects_data['game_menu']['sb'].data['chip_2'],
            self.objects_data['game_menu']['sb'].data['chip_3'], self.objects_data['game_menu']['sb'].data['chip_4'])
        for n, chip in enumerate(chips):
            if not chip:
                self.objects_data['game_menu']['sb'].data[f'chip_{n + 1}'] = True
                break

    def run_action(self, side: str) -> None:
        '''Метод бега'''
        self.other_data['move'] = True
        self.player.set_face_side(side)

    def stand_action(self):
        '''Метод бездействия'''
        self.other_data['move'] = False

    # ---------сектор действий кнопок меню---------

    def end_menu(self) -> None:
        '''Метод выхода из игрового меню'''
        data = JsonReader.read_file('../../data/json/units_data.json')
        if not self.other_data['in_door']:
            data[f'unit_{self.world_number}']['position'] = self.player.get_position_fr()
        data[f'unit_{self.world_number}']['player'] = self.objects_data['game_menu']['sb'].get_player_data()
        s, d, i, fp = self.objects_data['characteristic_menu']['cu'].get_characteristics()
        data[f'unit_{self.world_number}']['player']['str'] = s
        data[f'unit_{self.world_number}']['player']['int'] = i
        data[f'unit_{self.world_number}']['player']['dex'] = d
        data[f'unit_{self.world_number}']['player']['free_points'] = fp
        fg, fl, mp = self.objects_data['magic_menu']['mu'].get_characteristics()
        data[f'unit_{self.world_number}']['player']['fb_get'] = fp
        data[f'unit_{self.world_number}']['player']['fb_level'] = fl
        data[f'unit_{self.world_number}']['player']['magic_free_points'] = mp
        c_1, c_2, c_3, c_4 = self.objects_data['game_menu']['sb'].get_chips()
        data[f'unit_{self.world_number}']['player']['chip_1'] = c_1
        data[f'unit_{self.world_number}']['player']['chip_2'] = c_2
        data[f'unit_{self.world_number}']['player']['chip_3'] = c_3
        data[f'unit_{self.world_number}']['player']['chip_4'] = c_4
        JsonReader.write_file(data, '../../data/json/units_data.json')
        self.menu_process_flag = False
        self.other_data['move'] = False
        self.collision.clear()
        self.other_data['music_manager'].stop_sound('all')
        if self.present_menu == 'end_game_menu':
            data = JsonReader.read_file('../../data/json/units_data.json')
            data[f'unit_{self.world_number}']['world'] = []
            data[f'unit_{self.world_number}']['position'] = [0, 0]
            data[f'unit_{self.world_number}']['player'] = {"alive": 0, "level": 1, "max_level": 20, "exp": 0,
                                                           "exp_multiplier": 1.3, "min_hp": 100, "hp": 140,
                                                           "hp_multiplier": 1.4, "min_mp": 10, "mp": 11,
                                                           "mp_multiplier": 1.1, "str": 1, "dex": 1, "int": 1,
                                                           "free_points": 0, "fb_get": False, "fb_level": 0,
                                                           "magic_free_points": 0, 'chip_1': False, 'chip_2': False,
                                                           'chip_3': False, 'chip_4': False}
            JsonReader.write_file(data, '../../data/json/units_data.json')

    @click_sound
    def to_person_menu(self) -> None:
        '''Метод перехода в меню персоны'''
        self.other_data['move'] = False
        self.present_menu = 'persons_menu'

    @click_sound
    def to_map_menu(self) -> None:
        '''Метод переход в меню карты'''
        self.present_menu = 'map_menu'
        self.objects_data['map_menu']['bmp'].data['player_position'] = self.player.get_position_fr()
        self.objects_data['map_menu']['bmp'].data['camera_position'] = (0, 0)
        self.objects_data['map_menu']['bmp'].data['sector_size_multiplier'] = 1
        self.objects_data['map_menu']['bmp'].data['sector_size'] = 10
        self.objects_data['map_menu']['bmp'].change_render_frame()
        self.objects_data['map_menu']['bmp'].set_other_positions(self.enemies_generator.get_positions())
        self.other_data['move'] = False

    @click_sound
    def to_game_menu(self) -> None:
        '''Метод перехода в игровое меню'''
        self.present_menu = 'game_menu'

    @click_sound
    def to_upgrade_characteristics(self) -> None:
        '''Метод перехода в меню улучшений'''
        self.present_menu = 'characteristic_menu'
        self.inspect_add_buttons_ch()

    def inspect_add_buttons_ch(self) -> None:
        '''Метод проверки статусов кнопок'''
        if self.objects_data['characteristic_menu']['cu'].is_upgradeable():
            self.buttons_data['characteristic_menu']['add_str'].status = 'passive'
            self.buttons_data['characteristic_menu']['add_dex'].status = 'passive'
            self.buttons_data['characteristic_menu']['add_int'].status = 'passive'
        else:
            self.buttons_data['characteristic_menu']['add_str'].status = 'unactive'
            self.buttons_data['characteristic_menu']['add_dex'].status = 'unactive'
            self.buttons_data['characteristic_menu']['add_int'].status = 'unactive'

    @click_sound
    def add_fb(self) -> None:
        '''Метод улучшения магии'''
        self.objects_data['magic_menu']['mu'].add_point()
        self.inspect_add_buttons_m()

    def inspect_add_buttons_m(self) -> None:
        '''Метод проверки статусов магии'''
        if self.objects_data['magic_menu']['mu'].is_upgradeable():
            self.buttons_data['magic_menu']['add_fb'].status = 'passive'
        else:
            self.buttons_data['magic_menu']['add_fb'].status = 'unactive'

    @click_sound
    def to_upgrade_magic(self) -> None:
        '''Метод перехода в меню улучшения магии'''
        self.present_menu = 'magic_menu'
        self.inspect_add_buttons_m()

    @click_sound
    def add_str_point(self) -> None:
        '''Метод добавления очка сила'''
        self.add_characteristic_point('str')

    @click_sound
    def add_dex_point(self) -> None:
        '''Метод добавления очка ловкости'''
        self.add_characteristic_point('dex')

    @click_sound
    def add_int_point(self) -> None:
        '''Метод добавления очка интеллекта'''
        self.add_characteristic_point('int')

    def add_characteristic_point(self, characteristic) -> None:
        '''Метод добавления характеристики'''
        self.objects_data['characteristic_menu']['cu'].add_point(characteristic)
        self.inspect_add_buttons_ch()

    def start_battle(self, enemy) -> None:
        '''Метод старта битвы'''
        if enemy:
            self.other_data['music_manager'].stop_sound('all')
            self.other_data['move'] = False
            del self.enemies_generator[enemy]
            self.battle_thing.start_menu({'texture': '../../data/textures/player/test/right_run_0.png',
                                          'side': 'left',
                                          "hp": self.objects_data['game_menu']['sb'].data['hp'],
                                          "mp": self.objects_data['game_menu']['sb'].data['mp'],
                                          "level": self.objects_data['game_menu']['sb'].data['level'],
                                          "str": self.objects_data['characteristic_menu']['cu'].data['str_points'],
                                          "dex": self.objects_data['characteristic_menu']['cu'].data['dex_points'],
                                          "int": self.objects_data['characteristic_menu']['cu'].data['int_points'],
                                          "fb_level": self.objects_data['magic_menu']['mu'].data['fb_level'],
                                          'max_hp': self.objects_data['game_menu']['sb'].max_characteristic('hp'),
                                          'max_mp': self.objects_data['game_menu']['sb'].max_characteristic('mp')},
                                         enemy.battle_preparing())
            characteristics = self.battle_thing.get_ending_data()
            self.objects_data['game_menu']['sb'].data['hp'] = characteristics['hp']
            self.objects_data['game_menu']['sb'].data['mp'] = characteristics['mp']
            self.objects_data['game_menu']['sb'].data['exp'] += characteristics['exp']
            self.objects_data['game_menu']['sb'].dead_check()
            if self.objects_data['game_menu']['sb'].data['persona_status']:
                self.objects_data['game_menu']['sb'].level_up_check()
                mp, sp = self.objects_data['game_menu']['sb'].get_points()
                self.objects_data['game_menu']['sb'].clear_points()

                self.objects_data['magic_menu']['mu'].data['free_points'] = mp
                self.objects_data['magic_menu']['mu'].update_points()

                self.objects_data['characteristic_menu']['cu'].data['free_points'] = sp
                self.objects_data['characteristic_menu']['cu'].update_points()
            self.other_data['music_manager'].activate_music('middle_piano')

    def enter_in_door(self, number: str) -> None:
        '''Метод входа в подземелье'''
        self.door_layout = self.doors[number]
        places = []
        for n, y in enumerate(self.door_layout[0]):
            for m, x in enumerate(y):
                if x != 0:
                    places.append((m, n))
        self.number = number
        self.enemies_generator.clear()
        self.enemies_generator.set_world(self.door_layout)
        data = JsonReader.read_file('../../data/json/units_data.json')
        data[f'unit_{self.world_number}']['position'] = self.player.get_position()
        JsonReader.write_file(data, '../../data/json/units_data.json')
        place = random.choice(places)
        self.player.position = [place[0] * 100 - 960, place[1] * 100 - 540]
        self.collision.clear_blocks()

        self.add_collision_blocks(self.door_layout[0])

        self.objects_data['game_menu']['mp'].set_world_map(
            JsonReader.read_file('../../data/json/units_data.json')[f'unit_{self.world_number}']['doors'][number])
        self.objects_data['game_menu']['mp'].set_player_position(self.player.position)
        self.objects_data['map_menu']['bmp'].data['world_map'] = (
            self.objects_data['game_menu']['mp'].data['world_map'])
        self.objects_data['map_menu']['bmp'].data['world_size'] = self.objects_data['game_menu']['mp'].data[
            'world_size']
        self.world.set_world(self.other_data['generator'].texturing(
            JsonReader.read_file('../../data/json/units_data.json')[f'unit_{self.world_number}']['doors'][number]))

        self.other_data['in_door'] = True

    def enter_in_world(self) -> None:
        '''Метод входа в мир'''
        self.enemies_generator.clear()
        self.enemies_generator.set_world(self.sample_world)
        self.player.position = JsonReader.read_file('../../data/json/units_data.json')[f'unit_{self.world_number}'][
            'position']

        self.collision.clear_blocks()
        self.add_collision_blocks(self.sample_world[0])

        self.objects_data['game_menu']['mp'].set_world_map(self.sample_world)
        self.objects_data['game_menu']['mp'].set_player_position(self.player.position)
        self.objects_data['map_menu']['bmp'].data['world_map'] = (
            self.objects_data['game_menu']['mp'].data['world_map'])
        self.objects_data['map_menu']['bmp'].data['world_size'] = self.objects_data['game_menu']['mp'].data[
            'world_size']

        self.world.set_world(self.other_data['generator'].texturing(
            JsonReader.read_file('../../data/json/units_data.json')[f'unit_{self.world_number}']['world']))

        self.door_layout = None

        self.other_data['in_door'] = False

    def game_end(self) -> None:
        '''Метод окончания игры'''
        self.other_data['move'] = False
        self.present_menu = 'end_game_menu'
        charact = [self.objects_data['game_menu']['sb'].data['level'],
                   self.objects_data['characteristic_menu']['cu'].data['str_points'],
                   self.objects_data['characteristic_menu']['cu'].data['dex_points'],
                   self.objects_data['characteristic_menu']['cu'].data['int_points'],
                   self.objects_data['magic_menu']['mu'].data['fb_level']]
        self.buttons_data['end_game_menu']['level_up'].text = f'level: {charact[0]}'
        self.buttons_data['end_game_menu']['str_up'].text = f'str: {charact[1]}'
        self.buttons_data['end_game_menu']['dex_up'].text = f"dex: {charact[2]}"
        self.buttons_data['end_game_menu']['int_up'].text = f'int: {charact[3]}'
        self.buttons_data['end_game_menu']['magic_up'].text = f"magic: {charact[4]}"

from sys import exit

import pygame.image
from pygame import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, KEYDOWN, KEYUP, K_x, K_u, K_m
from pygame.display import update
from pygame.event import get

from json_reader import JsonReader
from buttons_menu import ButtonsMenu
from player import Player
from world import World
from custom_object_buttons import StatusBar, WorldMap, SkillUpgrade, MagicUpgrade, BigMap


class GameButtonsMenu(ButtonsMenu):
    def __init__(self, screen, clock, frame_rate, buttons_file_path, sample_world=None, player_data=None, world_number=None):
        super().__init__(screen=screen, clock=clock, frame_rate=frame_rate, buttons_file_path=buttons_file_path)
        self.add_other_data(move=False, background = pygame.image.load('..//..//data//textures//backgrounds//backgorund.png').convert(),
                            pressed_mouse_map=False, fps_counter=True, fps_font=pygame.font.SysFont('Comic Sans MS', 30))
        self.add_button_bind(back_button=self.end_menu,
                             person_menu_enter_button=self.to_person_menu,
                             map_menu_enter_button=self.to_map_menu,
                             back_to_game=self.to_game_menu,
                             to_upgrade_characteristics=self.to_upgrade_characteristics,
                             to_upgrade_magic=self.to_upgrade_magic,
                             add_str=self.add_str_point,
                             add_dex=self.add_dex_point,
                             add_int=self.add_int_point,
                             add_fb=self.add_fb)
        self.keys_dict = {1073741903: 'right', 1073741904: 'left', 1073741906: 'up', 1073741905: 'down'}
        self.world = None
        self.player = None
        self.sample_world = sample_world
        self.player_data = player_data
        self.world_number = world_number
        self.create_button_objects()

    def create_button_objects(self):
        objects_sb = self.objects_data['game_menu']['sb']
        self.objects_data['game_menu']['sb'] = StatusBar(self.screen,
                                                         *tuple(map(lambda name: objects_sb[name], objects_sb)))
        objects_mp = self.objects_data['game_menu']['mp']
        self.objects_data['game_menu']['mp'] = WorldMap(self.screen,
                                                        *tuple(map(lambda name: objects_mp[name], objects_mp)))
        objects_cu = self.objects_data['characteristic_menu']['cu']
        self.objects_data['characteristic_menu']['cu'] = SkillUpgrade(self.screen,
                                                        *tuple(map(lambda name: objects_cu[name], objects_cu)))

        objects_mu = self.objects_data['magic_menu']['mu']
        self.objects_data['magic_menu']['mu'] = MagicUpgrade(self.screen,
                                                        *tuple(map(lambda name: objects_mu[name], objects_mu)))

        self.objects_data['map_menu'] = {}
        self.objects_data['map_menu']['bmp'] = BigMap(self.screen)

    def create_world(self, world):
        self.world = World(self.screen, world)

    def create_player(self, person, position):
        self.player = Player(self.screen, position, person)

        self.objects_data['game_menu']['sb'].born()

    def start_menu(self, frame_rate) -> None:
        self.frame_rate = frame_rate
        self.objects_data['game_menu']['mp'].set_world_map(self.sample_world)
        self.objects_data['map_menu']['bmp'].data['world_map'] = (self.objects_data['game_menu']['mp'].data['world_map'])
        self.player.change_animation_under_fps(self.frame_rate)
        self.objects_data['game_menu']['sb'].add_data(**self.player_data)
        self.objects_data['characteristic_menu']['cu'].add_data(**self.objects_data['game_menu']['sb'].get_characteristics())
        self.objects_data['characteristic_menu']['cu'].add_data(
            **self.objects_data['game_menu']['sb'].get_characteristics())
        self.objects_data['characteristic_menu']['cu'].update_points()
        self.objects_data['magic_menu']['mu'].add_data(
            **self.objects_data['game_menu']['sb'].get_magic_data())
        self.objects_data['magic_menu']['mu'].update_points()
        self.menu_process_flag = True
        self.present_menu = 'game_menu'
        self.menu_process()

    def menu_process(self) -> None:
        while self.menu_process_flag:
            if self.present_menu == 'game_menu':
                self.game_unit()
                self.objects_data['game_menu']['sb'].dead_check()
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
        self.screen.blit(self.other_data['background'], (0, 0))

    def game_unit(self) -> None:
        self.screen.fill('white')
        self.world.draw_world(self.player.get_position())
        self.player.draw_player()

    def draw_fps(self):
        if self.other_data['fps_counter']:
            text = self.other_data['fps_font'].render(str(int(self.clock.get_fps())),True, 'red')
            self.screen.blit(text, (960, 10))

    def cursor_reader(self) -> None:
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
                        self.objects_data['characteristic_menu']['cu'].data['free_points'] = 1
                        self.objects_data['characteristic_menu']['cu'].update_points()
                    if event.key == K_m:
                        self.objects_data['magic_menu']['mu'].data['free_points'] +=  1
                        self.objects_data['magic_menu']['mu'].update_points()
                elif event.type == KEYUP:
                    if self.keys_dict.get(event.key, False) or not self.objects_data['game_menu'][
                        'sb'].get_persona_status():
                        self.player.clear_frame_skip()
                        self.stand_action()
            if self.present_menu == 'map_menu':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.objects_data['map_menu']['bmp'].change_sector_size(0.2)
                    elif event.button == 5:
                        self.objects_data['map_menu']['bmp'].change_sector_size(-0.2)

                    if self.objects_data['map_menu']['bmp'].in_map(event.pos):
                        self.other_data['pressed_mouse_map'] = True
                elif event.type == pygame.MOUSEMOTION:
                    if self.other_data['pressed_mouse_map']:
                        self.objects_data['map_menu']['bmp'].position_move(event.rel)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.other_data['pressed_mouse_map'] = False
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
            self.player.player_move('run')
        else:
            self.player.player_move('stand')

    def run_action(self, side):
        self.other_data['move'] = True
        self.player.set_face_side(side)

    def stand_action(self):
        self.other_data['move'] = False

    # ---------сектор действий кнопок меню---------

    def end_menu(self) -> None:
        data = JsonReader.read_file('../../data/json/units_data.json')
        data[f'unit_{self.world_number}']['position'] = self.player.get_position()
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
        JsonReader.write_file(data, '../../data/json/units_data.json')
        self.menu_process_flag = False
        self.other_data['move'] = False

    def to_person_menu(self):
        self.present_menu = 'persons_menu'

    def to_map_menu(self):
        self.present_menu = 'map_menu'
        self.objects_data['map_menu']['bmp'].data['player_position'] = self.objects_data['game_menu']['mp'].data['player_position']
        self.objects_data['map_menu']['bmp'].data['camera_position'] = (0, 0)
        self.objects_data['map_menu']['bmp'].data['sector_size_multiplier'] = 1
        self.objects_data['map_menu']['bmp'].data['sector_size'] = 10
        self.objects_data['map_menu']['bmp'].change_render_frame()

    def to_game_menu(self):
        self.present_menu = 'game_menu'

    def to_upgrade_characteristics(self):
        self.present_menu = 'characteristic_menu'
        self.inspect_add_buttons_ch()


    def inspect_add_buttons_ch(self):
        if self.objects_data['characteristic_menu']['cu'].is_upgradeable():
            self.buttons_data['characteristic_menu']['add_str'].status = 'passive'
            self.buttons_data['characteristic_menu']['add_dex'].status = 'passive'
            self.buttons_data['characteristic_menu']['add_int'].status = 'passive'
        else:
            self.buttons_data['characteristic_menu']['add_str'].status = 'unactive'
            self.buttons_data['characteristic_menu']['add_dex'].status = 'unactive'
            self.buttons_data['characteristic_menu']['add_int'].status = 'unactive'

    def add_fb(self):
        self.objects_data['magic_menu']['mu'].add_point()
        self.inspect_add_buttons_m()

    def inspect_add_buttons_m(self):
        if self.objects_data['magic_menu']['mu'].is_upgradeable():
            self.buttons_data['magic_menu']['add_fb'].status = 'passive'
        else:
            self.buttons_data['magic_menu']['add_fb'].status = 'unactive'

    def to_upgrade_magic(self):
        self.present_menu = 'magic_menu'
        self.inspect_add_buttons_m()

    def add_str_point(self):
        self.add_characteristic_point('str')

    def add_dex_point(self):
        self.add_characteristic_point('dex')

    def add_int_point(self):
        self.add_characteristic_point('int')

    def add_characteristic_point(self, characteristic):
        self.objects_data['characteristic_menu']['cu'].add_point(characteristic)
        self.inspect_add_buttons_ch()




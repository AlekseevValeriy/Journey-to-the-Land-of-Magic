from pygame.font import SysFont
from pygame import MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT
from pygame.event import get
from pygame.image import load
from sys import exit

from buttons_menu import ButtonsMenu
from game_buttons_menu import GameButtonsMenu
from json_reader import JsonReader
from world_generator import WorldGenerator
from player import Player
from music_manager import MusicManager





class StartButtonsMenu(ButtonsMenu):
    def __init__(self, screen, clock, frame_rate, buttons_file_path):
        super().__init__(screen=screen, clock=clock, frame_rate=frame_rate, buttons_file_path=buttons_file_path)
        self.add_other_data(background=load("../../data/textures/backgrounds/background.png").convert_alpha(),
                            volume_flag=False, fps_counter=True, fps_font=SysFont('Comic Sans MS', 30),
                            music_manager=MusicManager(0.5), present_volume=0)
        self.add_button_bind(exit_button=self.end_program,
                             credits_button=self.change_menu_credits,
                             settings_button=self.change_menu_settings,
                             worlds_button=self.change_menu_worlds,
                             back_button=self.change_menu_back,
                             fps_60_button=self.set_60_frame_rate,
                             fps_30_button=self.set_30_frame_rate,
                             fps_counter_yes_button=self.turn_on_fps_counter,
                             fps_counter_no_button=self.turn_off_fps_counter)
        self.buttons_data['settings_menu']['volume_trigger'].position[0] = (
            JsonReader.read_file('../../data/json/settings_data.json'))['volume_trigger_position']
        self.set_volume((self.buttons_data['settings_menu']['volume_trigger'].position[0]))
        self.other_data['music_manager'].activate_music('little_piano')

    def click_sound(function):
        def click(self, *args, **kwargs):
            function(self, *args, **kwargs)
            self.other_data['music_manager'].activate_effect('click')
        return click

    def start_menu(self) -> None:
        self.present_menu = 'start_menu'
        self.menu_process()

    def draw_background(self) -> None:
        self.screen.blit(self.other_data['background'], (0, 0))

    def draw_fps(self):
        if self.other_data['fps_counter']:
            text = self.other_data['fps_font'].render(str(int(self.clock.get_fps())), True, 'gray')
            self.screen.blit(text, (1879, 5))

    def cursor_reader(self) -> None:
        for event in get():
            if event.type == QUIT:
                self.end_program()
            elif event.type == MOUSEMOTION:
                buttons = self.buttons_data[self.present_menu]
                for button in buttons:
                    if event.pos in buttons[button] and not buttons[button].status == 'unactive':
                        buttons[button].status = 'active'
                    else:
                        if buttons[button].status == 'active':
                            buttons[button].status = 'passive'
                if self.other_data['volume_flag']:
                    x = event.pos[0]
                    if x < 816:
                        x = 816
                    elif x >= 1100:
                        x = 1100
                    self.buttons_data['settings_menu']['volume_trigger'].position[0] = x - 19
                    self.set_volume(x)

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons = self.buttons_data[self.present_menu]
                    for button in buttons:
                        if event.pos in buttons[button]:
                            if button == 'volume_trigger':
                                self.other_data['volume_flag'] = True
                                self.other_data['music_manager'].activate_effect('click')
                            if not buttons[button].status == 'unactive':
                                if 'world_' in button and not 'title' in button:
                                    self.special_world_work(button)
                                else:
                                    self.buttons_binds.get(button, self.not_found_function)()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if self.present_menu == 'settings_menu':
                        if self.other_data['volume_flag']:
                            self.other_data['volume_flag'] = False

    def set_volume(self, value):
        value = (value - 816) * 100 // (1100 - 816) / 100
        if value > 1:
            value = 1
        if value < 0:
            value = 0
        self.other_data['music_manager'].set_volume(value)

    # ---------сектор действий кнопок меню---------

    @click_sound
    def end_program(self):
        print('program registered end')
        self.menu_process_flag = False
        exit()

    def not_found_function(self):
        print('Not found')

    @click_sound
    def change_menu_settings(self):
        self.present_menu = 'settings_menu'

    @click_sound
    def change_menu_credits(self):
        self.present_menu = 'credits'

    @click_sound
    def change_menu_worlds(self):
        self.present_menu = 'worlds'
        self.unactive_inspector()

    def unactive_inspector(self):
        worlds_data = JsonReader.read_file('../../data/json/units_data.json')
        for n, world in enumerate(worlds_data):
            if worlds_data[world]['world']:
                self.buttons_data[self.present_menu][f'world_button_{n + 1}'].text = 'Войти'
                self.buttons_data[self.present_menu][f'world_button_{n + 1}'].status = 'passive'
                self.buttons_data[self.present_menu][f'world_create_{n + 1}'].status = 'unactive'
                self.buttons_data[self.present_menu][f'world_delete_{n + 1}'].status = 'passive'
            else:
                self.buttons_data[self.present_menu][f'world_button_{n + 1}'].text = 'Пустой'
                self.buttons_data[self.present_menu][f'world_button_{n + 1}'].status = 'unactive'
                self.buttons_data[self.present_menu][f'world_create_{n + 1}'].status = 'passive'
                self.buttons_data[self.present_menu][f'world_delete_{n + 1}'].status = 'unactive'

    @click_sound
    def special_world_work(self, name):
        if 'button' in name:
            self.start_game_process(
                JsonReader.read_file('../../data/json/units_data.json')[f'unit_{name[-1]}']['world'],
                JsonReader.read_file('../../data/json/units_data.json')[f'unit_{name[-1]}']['player'],
                int(name[-1]))
        elif 'delete' in name:
            data = JsonReader.read_file('../../data/json/units_data.json')
            data[f'unit_{name[-1]}']['world'] = []
            data[f'unit_{name[-1]}']['position'] = [0, 0]
            data[f'unit_{name[-1]}']['player'] = {"alive": 0, "level": 1, "max_level": 20, "exp": 0,
                                                  "exp_multiplier": 1.3, "min_hp": 100, "hp": 140, "hp_multiplier": 1.4,
                                                  "min_mp": 10,
                                                  "mp": 11, "mp_multiplier": 1.1, "str": 1, "dex": 1, "int": 1,
                                                  "free_points": 0, "fb_get": False, "fb_level": 0,
                                                  "magic_free_points": 0}

            JsonReader.write_file(data, '../../data/json/units_data.json')
        elif 'create' in name:
            data = JsonReader.read_file('../../data/json/units_data.json')
            world = WorldGenerator()
            world.create_world()
            data[f'unit_{name[-1]}']['world'] = world.get_world()
            data[f'unit_{name[-1]}']['position'] = Player.position_as_sp(world.set_random_player_position())
            JsonReader.write_file(data, '../../data/json/units_data.json')
        self.unactive_inspector()

    @click_sound
    def change_menu_back(self):
        if self.present_menu == 'settings_menu':
            data = JsonReader.read_file('../../data/json/settings_data.json')
            data['fps'] = self.frame_rate
            data['volume_trigger_position'] = self.buttons_data['settings_menu']['volume_trigger'].position[0]
            JsonReader.write_file(data, '../../data/json/settings_data.json')
        self.present_menu = 'start_menu'

    @click_sound
    def set_60_frame_rate(self):
        self.frame_rate = 60

    @click_sound
    def set_30_frame_rate(self):
        self.frame_rate = 30

    def create_game_process(self):
        game = GameButtonsMenu(self.screen, self.clock, self.frame_rate,
                               '../../data/json/game_buttons_data.json', )
        self.add_other_data(game_process=game, game_flag=False)

    def start_game_process(self, world_layout, player_data, world_number):
        if 'game_flag' not in self.other_data:
            self.create_game_process()
        if 'game_flag' in self.other_data and not self.other_data['game_flag']:
            generator = WorldGenerator()
            self.other_data['game_process'].sample_world = JsonReader.read_file('../../data/json/units_data.json')[f'unit_{world_number}']['world']
            self.other_data['game_process'].player_data = player_data
            self.other_data['game_process'].world_number = world_number
            self.other_data['game_process'].create_world(generator.texturing(world_layout[:]))
            position = JsonReader.read_file('../../data/json/units_data.json')[f'unit_{world_number}']['position']
            if position[0] == 0 and position[1] == 0:
                position = [-self.screen.get_width() // 2, -self.screen.get_height() // 2]
            self.other_data['game_process'].create_player('test', position)
            data = JsonReader.read_file('../../data/json/units_data.json')[f'unit_{world_number}']['player']
            self.other_data['game_process'].objects_data['game_menu']['sb'].add_data(**data)
            self.other_data['game_process'].other_data['fps_counter'] = self.other_data['fps_counter']
        self.other_data['game_process'].start_menu(self.frame_rate)
        self.other_data['game_flag'] = False


    @click_sound
    def turn_on_fps_counter(self):
        self.other_data['fps_counter'] = True

    @click_sound
    def turn_off_fps_counter(self):
        self.other_data['fps_counter'] = False

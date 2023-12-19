from pygame import MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, QUIT
from pygame.event import get
from pygame.image import load
from sys import exit


from buttons_menu import ButtonsMenu
from game_buttons_menu import GameButtonsMenu
from json_reader import JsonReader
from world_generator import WorldGenerator


class StartButtonsMenu(ButtonsMenu):
    def __init__(self, screen, clock, frame_rate, buttons_file_path):
        super().__init__(screen=screen, clock=clock, frame_rate=frame_rate, buttons_file_path=buttons_file_path)
        self.add_other_data(background=load("../../data/textures/backgrounds/backgorund.png").convert_alpha(),
                            volume_flag=False)
        self.add_button_bind(exit_button=self.end_program,
                             credits_button=self.change_menu_credits,
                             settings_button=self.change_menu_settings,
                             worlds_button=self.change_menu_worlds,
                             back_button=self.change_menu_back,
                             fps_60_button=self.set_60_frame_rate,
                             fps_30_button=self.set_30_frame_rate)

    def start_menu(self) -> None:
        self.present_menu = 'start_menu'
        self.menu_process()

    def draw_background(self) -> None:
        self.screen.blit(self.other_data['background'], (0, 0))

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
                    if x <= 495:
                        self.buttons_data['settings_menu']['volume_trigger'].position[0] = 495
                    elif x >= 775:
                        self.buttons_data['settings_menu']['volume_trigger'].position[0] = 775
                    else:
                        self.buttons_data['settings_menu']['volume_trigger'].position[0] = x
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons = self.buttons_data[self.present_menu]
                    for button in buttons:
                        if event.pos in buttons[button]:
                            if button == 'volume_trigger':
                                self.other_data['volume_flag'] = True
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

    # ---------сектор действий кнопок меню---------

    def end_program(self):
        print('program registered end')
        self.menu_process_flag = False
        exit()

    def not_found_function(self):
        print('Not found')

    def change_menu_settings(self):
        self.present_menu = 'settings_menu'

    def change_menu_credits(self):
        self.present_menu = 'credits'

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

    def special_world_work(self, name):
        if 'button' in name:
            self.start_game_process(
                JsonReader.read_file('../../data/json/units_data.json')[f'unit_{name[-1]}']['world'])
        elif 'delete' in name:
            data = JsonReader.read_file('../../data/json/units_data.json')
            data[f'unit_{name[-1]}']['world'] = []
            JsonReader.write_file(data, '../../data/json/units_data.json')
        elif 'create' in name:
            data = JsonReader.read_file('../../data/json/units_data.json')
            world = WorldGenerator()
            world.test_create_world()
            data[f'unit_{name[-1]}']['world'] = world.get_world()
            JsonReader.write_file(data, '../../data/json/units_data.json')
        self.unactive_inspector()

    def change_menu_back(self):
        self.present_menu = 'start_menu'

    def set_60_frame_rate(self):
        self.frame_rate = 60

    def set_30_frame_rate(self):
        self.frame_rate = 30

    def create_game_process(self):
        game = GameButtonsMenu(self.screen, self.clock, self.frame_rate,
                               '../../data/json/game_buttons_data.json')
        self.add_other_data(game_process=game, game_flag=False)

    def start_game_process(self, world_layout):
        if 'game_flag' not in self.other_data:
            self.create_game_process()
        if 'game_flag' in self.other_data and not self.other_data['game_flag']:
            generator = WorldGenerator()
            self.other_data['game_process'].sample_world = world_layout
            world_layout = generator.texturing(world_layout)
            self.other_data['game_process'].create_world(world_layout)
            self.other_data['game_process'].create_player('test', [-self.screen.get_width() // 2, -self.screen.get_height() // 2])
        self.other_data['game_process'].start_menu()
        self.other_data['game_flag'] = False

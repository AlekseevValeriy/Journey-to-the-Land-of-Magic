import pygame

from button import Button
from parameter_reader import ParameterReaderRead
from player import Player
from world import World

"""
Класс, который визуализирует игровой процесс, а также считывает все действия 
"""

class GameProcess:
    def __init__(self, game_screen, fps, clock, language, world_layout, player_coordinate):
        self.game_screen = game_screen
        self.fps = fps
        self.clock = clock
        self.language = language
        self.buttons_information = ParameterReaderRead('game_process.json', file_path='settings').load_parameters()
        self.button_library = {}
        self.list_of_translations = ParameterReaderRead("list_of_translations.json",
                                                        file_path='settings').load_parameters()
        player_coordinate = [player_coordinate[0] * 34 + 43,
                             player_coordinate[1] * 54 + 81]  # начальная позиция [43, 81]
        self.world = World(self.game_screen, [34, 54], world_layout, player_coordinate)
        self.player = Player(self.game_screen, self.fps, player_coordinate)
        self.game_flag = True
        self.pressed_buttons = {'up': [False, 'y', '-'], 'down': [False, 'y', '+'], 'left': [False, 'x', '-'],
                                'right': [False, 'x', '+']}
        self.frame_rate_counter = 0

    def checking_actions(self, event_outer):
        for event in event_outer:
            # TODO если будет много, то укорочу с помощью списков и циклов
            keys = pygame.key.get_pressed()
            self.pressed_buttons['up'][0] = True if keys[pygame.K_UP] else False
            self.pressed_buttons['down'][0] = True if keys[pygame.K_DOWN] else False
            self.pressed_buttons['left'][0] = True if keys[pygame.K_LEFT] else False
            self.pressed_buttons['right'][0] = True if keys[pygame.K_RIGHT] else False

            if event.type == pygame.MOUSEMOTION:
                mouse_coordinate = event.pos
                for button in self.button_library:
                    button_size = self.button_library[button].texture_size
                    if (self.button_library[button].coordinate[0] <= mouse_coordinate[0] <= (
                            self.button_library[button].coordinate[0] + button_size[0])) and (
                            self.button_library[button].coordinate[1] <= mouse_coordinate[1] <= (
                            self.button_library[button].coordinate[1] + button_size[1])):
                        self.button_library[button].status = 'active'
                    else:
                        self.button_library[button].status = 'passive'
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coordinate = event.pos
                for button in self.button_library:
                    button_size = self.button_library[button].texture_size
                    if (self.button_library[button].coordinate[0] <= mouse_coordinate[0] <= (
                            self.button_library[button].coordinate[0] + button_size[0])) and (
                            self.button_library[button].coordinate[1] <= mouse_coordinate[1] <= (
                            self.button_library[button].coordinate[1] + button_size[1])) and event.button == 1:
                        if button == 'button_menu':
                            self.game_flag = False

        control_actions = []
        for button in self.pressed_buttons:
            if self.pressed_buttons[button][0]:
                control_actions.append(True)
                self.player.player_side = button
                self.player.change_position(self.pressed_buttons[button][1], self.player.player_motion_step,
                                            self.pressed_buttons[button][2])
                self.world.set_player_coordinate(self.player.get_position())
            else:
                control_actions.append(False)
        self.player.status = 'worth' if not any(control_actions) else 'run'

    def animation_calculator(self):
        self.frame_rate_counter = self.frame_rate_counter % self.fps + 1

    def set_buttons_information(self):
        for button in self.buttons_information:
            button_inf = self.buttons_information[button]
            self.button_library[button] = Button(self.game_screen, button_inf['texture'], button_inf['font'],
                                                 button_inf['font_size'], button_inf['text'],
                                                 button_inf['coordinate'], button_inf['font_color_1'],
                                                 button_inf['font_color_2'], button_inf['status'])
        if self.language == 'ru':
            for button in self.button_library:
                old_text = self.button_library[button].text
                self.button_library[button].text = self.list_of_translations['game_process'][old_text]

    def drawing_buttons(self):
        [self.button_library[button].draw_button() for button in self.button_library]

    def set_fps(self):
        self.button_library['fps_counter'].text = str(int(self.clock.get_fps()))

    def game_process(self):
        self.set_buttons_information()
        while self.game_flag:
            self.checking_actions(pygame.event.get())
            self.animation_calculator()
            self.world.draw_world()
            self.player.draw_player(self.frame_rate_counter)
            self.set_fps()
            self.drawing_buttons()
            pygame.display.update()
            self.clock.tick(self.fps)

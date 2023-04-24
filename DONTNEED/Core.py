import random

import pygame.display

import map_generation

from supportiveDrawMenuStage import *
"""import settings"""
#TODO переделать генерацию карты. Сделать основу на 'for _ in' и рандомно выбирать допустимые участки.
with open('parameter.txt') as f:
    file = f.readlines()

    window = file[3].rstrip().lstrip('@').split('.')
    window_x_size, window_y_size = int(window[0]), int(window[1])

    game_map = file[5].rstrip().lstrip('@').split('.')
    map_x_size, map_y_size = int(game_map[0]), int(game_map[1])

    sector = file[7].rstrip().lstrip('@').split('.')
    sector_x, sector_y = int(sector[0]), int(sector[1])


class GameProcess:
    def __init__(self, window_size, map_size, sector_size, quantity_of_points):
        pygame.font.init()
        pygame.display.init()
        pygame.init()
        self.window_size = window_size
        self.map_size = map_size
        self.sector_size = sector_size
        self.camera_x_position = self.window_size[0] // 2
        self.camera_y_position = self.window_size[1] // 2
        self.game_map = map_generation.MapGeneration(self.map_size[0], self.map_size[1],
                                                     quantity_of_points).map_create()
        self.dictionary_of_colors = {'background': (255, 255, 255), 'menu_background': (102, 102, 255),
                                     'setting_background': (255, 51, 255),
                                     'red': (255, 0, 0), 'blue': (0, 0, 255), 'b_g_1': (0, 102, 51),
                                     'back': (255, 102, 0)}
        for n in range(3):
            self.dictionary_of_colors[f'b_m_{n}'] = (51, 255, 255)
        for n in range(8):
            self.dictionary_of_colors[f'b_e{n}'] = (204, 153, 102)
        for m in self.game_map:
            for n in m:
                if n not in self.dictionary_of_colors:
                    self.dictionary_of_colors[n] = (random.randint(0, 255), random.randint(0, 255),
                                                    random.randint(0, 255))

        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
        self.pygame_icon = pygame.image.load('icon.bmp')
        pygame.display.set_icon(self.pygame_icon)
        pygame.display.set_caption('.   by Valeriy Alekseev 9A')
        self.process_flag = True
        self.menu_process_flag = None
        self.setting_process_flag = None
        self.dictionary_of_fonts = {'standart_font': pygame.font.SysFont('Insight Sans SSi', 18),
                                    'FPS_font': pygame.font.Font('fonts/Samson.ttf', 50)}
        self.clock = pygame.time.Clock()
        self.FPS = 24
        self.power_of_move_gorizontal = 0
        self.power_of_move_vertical = 0
        self.entity_x_position = 0
        self.entity_y_position = 0
        self.step_of_move_entity = 10
        self.full_screen_toggle = False

    def check_position(self, pygame_event, mobject, sufferer, begin_x, end_x, begin_y, end_y):
        if mobject == 'mouse_position':
            position = pygame_event.pos
            if sufferer == 'game_button_menu':
                if begin_x <= position[0] <= end_x and begin_y <= position[1] <= end_y:
                    return True
                return False
        elif mobject == 'mouse_position + click':
            position = pygame_event.pos
            if sufferer == 'game_button_menu':
                if begin_x <= position[0] <= end_x and begin_y <= position[1] <= end_y and pygame_event.button == 1:
                    return True
                return False

    def action_check(self, pygame_event):
        for event in pygame_event:
            """exit click check"""
            if event.type == pygame.QUIT:
                pygame.quit()
                self.process_flag = False
            if event.type == pygame.MOUSEMOTION:
                if self.check_position(event, 'mouse_position', 'game_button_menu', self.window_size[0] * 0.1,
                                       self.window_size[0] * 0.1 + 70, self.window_size[1] * 0.05,
                                       self.window_size[1] * 0.05 + 40):
                    self.dictionary_of_colors['b_g_1'] = (0, 152, 51)
                else:
                    self.dictionary_of_colors['b_g_1'] = (0, 102, 51)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.check_position(event, 'mouse_position + click', 'game_button_menu', self.window_size[0] * 0.1,
                                       self.window_size[0] * 0.1 + 70, self.window_size[1] * 0.05,
                                       self.window_size[1] * 0.05 + 40):
                    self.dictionary_of_colors['b_g_1'] = (0, 102, 51)
                    draw_menu_stage(self, True)
        if self.process_flag:
            keys = pygame.key.get_pressed()
            """entity motions check (pressed)"""
            if keys[pygame.K_a]:
                self.entity_x_position -= self.step_of_move_entity
            if keys[pygame.K_d]:
                self.entity_x_position += self.step_of_move_entity
            if keys[pygame.K_w]:
                self.entity_y_position -= self.step_of_move_entity
            if keys[pygame.K_s]:
                self.entity_y_position += self.step_of_move_entity

    def physics(self):
        """entity motion calculate"""

        self.entity_x_position += self.power_of_move_gorizontal
        self.entity_y_position += self.power_of_move_vertical

        if self.power_of_move_gorizontal < 0:
            self.power_of_move_gorizontal += 0.1
        elif self.power_of_move_gorizontal > 0:
            self.power_of_move_gorizontal -= 0.1

        if self.power_of_move_vertical < 0:
            self.power_of_move_vertical += 0.1
        elif self.power_of_move_vertical > 0:
            self.power_of_move_vertical -= 0.1

    def draw_button(self, text, x_button, y_button, wieght, hight, color_button, font, x_font, y_font, color_font):
        if color_button != '_':
            pygame.draw.rect(self.screen, self.dictionary_of_colors[color_button], (x_button, y_button, wieght, hight))
        button_text = self.dictionary_of_fonts[font].render(text, True, self.dictionary_of_colors[color_font])
        self.screen.blit(button_text, (x_font, y_font))

    def draw_entity(self):
        """entity draw"""

        pygame.draw.rect(self.screen, self.dictionary_of_colors['red'], (self.camera_x_position, self.camera_y_position,
                                                                         10, 10))

    def draw_game_map(self, fill):
        """game map draw"""

        self.screen.fill((255, 255, 255))
        x = 0
        y = 0
        for row in self.game_map:
            for col in row:
                pygame.draw.rect(self.screen, tuple([i + fill if i + fill <= 255 else 255 for i in self.dictionary_of_colors[col]]), (
                    x - self.entity_x_position + self.camera_x_position,
                    y - self.entity_y_position + self.camera_y_position, self.sector_size[0], self.sector_size[1]))
                x += self.sector_size[0]
            y += self.sector_size[1]
            x = 0

    def draw_decor(self):
        """menu button draw"""

        pygame.draw.rect(self.screen, self.dictionary_of_colors['b_g_1'], (self.window_size[0] * 0.1,
                                                                                      self.window_size[1] * 0.05, 70,
                                                                                      40))
        """counter of fps draw"""

        text2 = self.dictionary_of_fonts['FPS_font'].render(str(int(self.clock.get_fps())), True,
                                                            self.dictionary_of_colors['blue'])
        self.screen.blit(text2, (50, 50))


    def core_process(self):
        """connection of all"""
        draw_menu_stage(self, False)
        while self.process_flag:
            self.action_check(pygame.event.get())
            if not self.process_flag:
                break
            # self.physics()
            self.draw_game_map(0)
            self.draw_entity()
            self.draw_decor()
            pygame.display.update()
            self.clock.tick(self.FPS)


game = GameProcess([window_x_size, window_y_size], [map_x_size, map_y_size], [sector_x, sector_y], [2, 5, 8])
game.core_process()

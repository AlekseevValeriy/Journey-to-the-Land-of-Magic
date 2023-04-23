import pygame


def draw_setting_stage(self):
    self.setting_process_flag = True
    while self.setting_process_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.menu_process_flag = False
                self.process_flag = False
            if event.type == pygame.MOUSEMOTION:
                """b_e0"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 8, self.window_size[0] // 8 + 60,
                                       self.window_size[1] // 29, self.window_size[1] // 29 + 30):
                    self.dictionary_of_colors['b_e0'] = (204, 153, 152)
                else:
                    self.dictionary_of_colors['b_e0'] = (204, 153, 102)
                """b_e1"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 5, self.window_size[0] // 5 + 80,
                                       self.window_size[1] // 29, self.window_size[1] // 29 + 30):
                    self.dictionary_of_colors['b_e1'] = (204, 153, 152)
                else:
                    self.dictionary_of_colors['b_e1'] = (204, 153, 102)
                """b_e2"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 3.4, self.window_size[0] // 3.4 + 70,
                                       self.window_size[1] // 29, self.window_size[1] // 29 + 30):
                    self.dictionary_of_colors['b_e2'] = (204, 153, 152)
                else:
                    self.dictionary_of_colors['b_e2'] = (204, 153, 102)
                """window"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 8, self.window_size[0] // 8 + 60,
                                       self.window_size[1] // 11, self.window_size[1] // 11 + 30):
                    self.dictionary_of_colors['b_e3'] = (204, 153, 152)
                else:
                    self.dictionary_of_colors['b_e3'] = (204, 153, 102)
                """full screen"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 5, self.window_size[0] // 5 + 80,
                                       self.window_size[1] // 11, self.window_size[1] // 11 + 30):
                    self.dictionary_of_colors['b_e4'] = (204, 153, 152)
                else:
                    self.dictionary_of_colors['b_e4'] = (204, 153, 102)
                """back"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 1.1, self.window_size[0] // 1.1 + 60,
                                       self.window_size[1] // 29, self.window_size[1] // 29 + 30):
                    self.dictionary_of_colors['back'] = (255, 102, 100)
                else:
                    self.dictionary_of_colors['back'] = (255, 102, 0)
                """24"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 8, self.window_size[0] // 8 + 60,
                                       self.window_size[1] // 7, self.window_size[1] // 7 + 30):
                    self.dictionary_of_colors['b_e5'] = (204, 153, 152)
                else:
                    self.dictionary_of_colors['b_e5'] = (204, 153, 102)
                """30"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 5, self.window_size[0] // 5 + 80,
                                       self.window_size[1] // 7, self.window_size[1] // 7 + 30):
                    self.dictionary_of_colors['b_e6'] = (204, 153, 152)
                else:
                    self.dictionary_of_colors['b_e6'] = (204, 153, 102)
                """60"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 3.4, self.window_size[0] // 3.4 + 70,
                                       self.window_size[1] // 7, self.window_size[1] // 7 + 30):
                    self.dictionary_of_colors['b_e7'] = (204, 153, 152)
                else:
                    self.dictionary_of_colors['b_e7'] = (204, 153, 102)
            if event.type == pygame.MOUSEBUTTONDOWN:
                """b_e0"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 8, self.window_size[0] // 8 + 60,
                                       self.window_size[1] // 29, self.window_size[1] // 29 + 30):
                    self.dictionary_of_colors['b_e0'] = (204, 153, 102)
                    self.window_size = [800, 600]
                    self.camera_x_position = self.window_size[0] // 2
                    self.camera_y_position = self.window_size[1] // 2
                    if self.full_screen_toggle:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]),
                                                              pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
                """b_e1"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 5, self.window_size[0] // 5 + 80,
                                       self.window_size[1] // 29, self.window_size[1] // 29 + 30):
                    self.dictionary_of_colors['b_e1'] = (204, 153, 102)
                    self.window_size = [1600, 900]
                    self.camera_x_position = self.window_size[0] // 2
                    self.camera_y_position = self.window_size[1] // 2
                    if self.full_screen_toggle:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]),
                                                              pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
                """b_e2"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 3.4, self.window_size[0] // 3.4 + 70,
                                       self.window_size[1] // 29, self.window_size[1] // 29 + 30):
                    self.dictionary_of_colors['b_e2'] = (204, 153, 102)
                    self.window_size = [1920, 1080]
                    self.camera_x_position = self.window_size[0] // 2
                    self.camera_y_position = self.window_size[1] // 2
                    if self.full_screen_toggle:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]),
                                                              pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
                """window"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 8, self.window_size[0] // 8 + 60,
                                       self.window_size[1] // 11, self.window_size[1] // 11 + 30):
                    self.full_screen_toggle = False
                    self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
                """full screen"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 5, self.window_size[0] // 5 + 80,
                                       self.window_size[1] // 11, self.window_size[1] // 11 + 30):
                    self.full_screen_toggle = True
                    self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]), pygame.FULLSCREEN | pygame.DOUBLEBUF)
                """exit"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 1.1, self.window_size[0] // 1.1 + 60,
                                       self.window_size[1] // 29, self.window_size[1] // 29 + 30):
                    self.dictionary_of_colors['exit'] = (255, 102, 0)
                    self.setting_process_flag = False
                """24"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 8, self.window_size[0] // 8 + 60,
                                       self.window_size[1] // 7, self.window_size[1] // 7 + 30):
                    self.dictionary_of_colors['b_e5'] = (204, 153, 102)
                    self.FPS = 24
                """30"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 5, self.window_size[0] // 5 + 80,
                                       self.window_size[1] // 7, self.window_size[1] // 7 + 30):
                    self.dictionary_of_colors['b_e6'] = (204, 153, 102)
                    self.FPS = 30
                """60"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 3.4, self.window_size[0] // 3.4 + 70,
                                       self.window_size[1] // 7, self.window_size[1] // 7 + 30):
                    self.dictionary_of_colors['b_e7'] = (204, 153, 102)
                    self.FPS = 60
        if not self.setting_process_flag or not self.process_flag:
            break
        keys = pygame.key.get_pressed()
        self.screen.fill(self.dictionary_of_colors['setting_background'])

        """Expansion"""
        self.draw_button('Expansion:', 0, 0, 0, 0, '_', 'standart_font', self.window_size[0] // 25,
                         self.window_size[1] // 25, 'red')

        self.draw_button('800X600', self.window_size[0] // 8, self.window_size[1] // 29, 60, 30,
                         'b_e0', 'standart_font', self.window_size[0] // 7.6, self.window_size[1] // 25, 'red')

        self.draw_button('1600X900', self.window_size[0] // 5, self.window_size[1] // 29, 80, 30,
                         'b_e1', 'standart_font', self.window_size[0] // 4.8, self.window_size[1] // 25, 'red')

        self.draw_button('1920X1080', self.window_size[0] // 3.4, self.window_size[1] // 29, 70, 30,
                         'b_e2', 'standart_font', self.window_size[0] // 3.4, self.window_size[1] // 25, 'red')

        """Screen mode"""
        self.draw_button('Screen mode:', 0, 0, 0, 0, '_', 'standart_font', self.window_size[0] // 25,
                         self.window_size[1] // 10, 'red')

        self.draw_button('window', self.window_size[0] // 8, self.window_size[1] // 11, 60, 30,
                         'b_e3', 'standart_font', self.window_size[0] // 7.6, self.window_size[1] // 10, 'red')

        self.draw_button('full screen', self.window_size[0] // 5, self.window_size[1] // 11, 80, 30,
                         'b_e4', 'standart_font', self.window_size[0] // 4.8, self.window_size[1] // 10, 'red')

        """FPS"""

        self.draw_button('FPS:', 0, 0, 0, 0, '_', 'standart_font', self.window_size[0] // 25,
                         self.window_size[1] // 25, 'red')

        self.draw_button('24', self.window_size[0] // 8, self.window_size[1] // 7, 60, 30,
                         'b_e5', 'standart_font', self.window_size[0] // 7.6 + 21, self.window_size[1] // 7 + 11, 'red')

        self.draw_button('30', self.window_size[0] // 5, self.window_size[1] // 7, 80, 30,
                         'b_e6', 'standart_font', self.window_size[0] // 4.8 + 24, self.window_size[1] // 7 + 11, 'red')

        self.draw_button('60', self.window_size[0] // 3.4, self.window_size[1] // 7, 70, 30,
                         'b_e7', 'standart_font', self.window_size[0] // 3.4 + 24, self.window_size[1] // 7 + 11, 'red')

        """Back"""
        self.draw_button('Back', self.window_size[0] // 1.1, self.window_size[1] // 29, 60, 30,
                         'back', 'standart_font', self.window_size[0] // 1.075, self.window_size[1] // 25, 'blue')

        pygame.display.update()

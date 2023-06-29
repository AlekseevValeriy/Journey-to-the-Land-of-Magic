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
                if self.buttons.check_position(event, 'b_e0'):
                    self.buttons.dictionary_of_parameters_button['b_e0'][4] = (204, 153, 152)
                else:
                    self.buttons.dictionary_of_parameters_button['b_e0'][4] = (204, 153, 102)
                """b_e1"""
                if self.buttons.check_position(event, 'b_e1'):
                    self.buttons.dictionary_of_parameters_button['b_e1'][4] = (204, 153, 152)
                else:
                    self.buttons.dictionary_of_parameters_button['b_e1'][4] = (204, 153, 102)
                """b_e2"""
                if self.buttons.check_position(event, 'b_e2'):
                    self.buttons.dictionary_of_parameters_button['b_e2'][4] = (204, 153, 152)
                else:
                    self.buttons.dictionary_of_parameters_button['b_e2'][4] = (204, 153, 102)
                """window"""
                if self.buttons.check_position(event, 'b_e3'):
                    self.buttons.dictionary_of_parameters_button['b_e3'][4] = (204, 153, 152)
                else:
                    self.buttons.dictionary_of_parameters_button['b_e3'][4] = (204, 153, 102)
                """full screen"""
                if self.buttons.check_position(event, 'b_e4'):
                    self.buttons.dictionary_of_parameters_button['b_e4'][4] = (204, 153, 152)
                else:
                    self.buttons.dictionary_of_parameters_button['b_e4'][4] = (204, 153, 102)
                """back"""
                if self.buttons.check_position(event, 'back'):
                    self.buttons.dictionary_of_parameters_button['back'][4] = (255, 102, 100)
                else:
                    self.buttons.dictionary_of_parameters_button['back'][4] = (255, 102, 0)
                """24"""
                if self.buttons.check_position(event, 'b_e5'):
                    self.buttons.dictionary_of_parameters_button['b_e5'][4] = (204, 153, 152)
                else:
                    self.buttons.dictionary_of_parameters_button['b_e5'][4] = (204, 153, 102)
                """30"""
                if self.buttons.check_position(event, 'b_e6'):
                    self.buttons.dictionary_of_parameters_button['b_e6'][4] = (204, 153, 152)
                else:
                    self.buttons.dictionary_of_parameters_button['b_e6'][4] = (204, 153, 102)
                """60"""
                if self.buttons.check_position(event, 'b_e7'):
                    self.buttons.dictionary_of_parameters_button['b_e7'][4] = (204, 153, 152)
                else:
                    self.buttons.dictionary_of_parameters_button['b_e7'][4] = (204, 153, 102)
                """volume"""
                if self.buttons.check_position(event, 'volume'):
                    self.buttons.dictionary_of_parameters_button['volume'][4] = (204, 153, 152)
                else:
                    self.buttons.dictionary_of_parameters_button['volume'][4] = (204, 153, 102)
            if event.type == pygame.MOUSEBUTTONDOWN:
                """b_e0"""
                if self.buttons.check_position(event, 'b_e0', mobject='mouse_position + click'):
                    self.dictionary_of_colors_core['b_e0'] = (204, 153, 102)
                    self.window_size = [800, 600]
                    self.camera_x_position = self.window_size[0] // 2
                    self.camera_y_position = self.window_size[1] // 2
                    if self.full_screen_toggle:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]),
                                                              pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
                    self.update_buttons()
                """b_e1"""
                if self.buttons.check_position(event, 'b_e1', mobject='mouse_position + click'):
                    self.dictionary_of_colors_core['b_e1'] = (204, 153, 102)
                    self.window_size = [1600, 900]
                    self.camera_x_position = self.window_size[0] // 2
                    self.camera_y_position = self.window_size[1] // 2
                    if self.full_screen_toggle:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]),
                                                              pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
                    self.update_buttons()
                """b_e2"""
                if self.buttons.check_position(event, 'b_e2', mobject='mouse_position + click'):
                    self.dictionary_of_colors_core['b_e2'] = (204, 153, 102)
                    self.window_size = [1920, 1080]
                    self.camera_x_position = self.window_size[0] // 2
                    self.camera_y_position = self.window_size[1] // 2
                    if self.full_screen_toggle:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]),
                                                              pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
                    self.update_buttons()
                """window"""
                if self.buttons.check_position(event, 'b_e3', mobject='mouse_position + click'):
                    self.buttons.dictionary_of_parameters_button['b_e3'][4] = (204, 153, 102)
                    self.full_screen_toggle = False
                    self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
                """full screen"""
                if self.buttons.check_position(event, 'b_e4', mobject='mouse_position + click'):
                    self.buttons.dictionary_of_parameters_button['b_e4'][4] = (204, 153, 102)
                    self.full_screen_toggle = True
                    self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]), pygame.FULLSCREEN | pygame.DOUBLEBUF)
                """back"""
                if self.buttons.check_position(event, 'back', mobject='mouse_position + click'):
                    self.buttons.dictionary_of_parameters_button['back'][4] = (204, 153, 0)
                    self.setting_process_flag = False
                """24"""
                if self.buttons.check_position(event, 'b_e5', mobject='mouse_position + click'):
                    self.buttons.dictionary_of_parameters_button['b_e5'][4] = (204, 153, 102)
                    self.FPS = 24
                    self.player.choice_fps(self.FPS)
                """30"""
                if self.buttons.check_position(event, 'b_e6', mobject='mouse_position + click'):
                    self.buttons.dictionary_of_parameters_button['b_e6'][4] = (204, 153, 102)
                    self.FPS = 30
                    self.player.choice_fps(self.FPS)
                """60"""
                if self.buttons.check_position(event, 'b_e7', mobject='mouse_position + click'):
                    self.buttons.dictionary_of_parameters_button['b_e7'][4] = (204, 153, 102)
                    self.FPS = 60
                    self.player.choice_fps(self.FPS)
                """volume"""
                if self.buttons.check_position(event, 'volume', mobject='mouse_position + press'):
                    self.buttons.dictionary_of_parameters_button['volume'][4] = (204, 153, 102)
        if not self.setting_process_flag or not self.process_flag:
            break
        keys = pygame.key.get_pressed()
        self.screen.fill(self.dictionary_of_colors_core['setting_background'])

        """Expansion"""
        self.buttons.draw_button(self.screen, 'exp', 'Expansion:')
        self.buttons.draw_button(self.screen, 'b_e0', '800X600')
        self.buttons.draw_button(self.screen, 'b_e1', '1600X900')
        self.buttons.draw_button(self.screen, 'b_e2', '1920X1080')
        """Screen mode"""
        self.buttons.draw_button(self.screen, 's_m', 'Screen mode:')
        self.buttons.draw_button(self.screen, 'b_e3', 'window')
        self.buttons.draw_button(self.screen, 'b_e4', 'full screen')
        """FPS"""
        self.buttons.draw_button(self.screen, 'fps', 'FPS:')
        self.buttons.draw_button(self.screen, 'b_e5', '24')
        self.buttons.draw_button(self.screen, 'b_e6', '30')
        self.buttons.draw_button(self.screen, 'b_e7', '60')
        """Back"""
        self.buttons.draw_button(self.screen, 'back', 'Back')
        """volume"""
        self.buttons.draw_button(self.screen, 'volume_s', 'Volume:')
        self.buttons.draw_special_button_volume(self.screen, 'volume')

        pygame.display.update()

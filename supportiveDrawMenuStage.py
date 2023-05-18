import pygame.mixer

from supportiveDrawSettingStage import *
def draw_menu_stage(self, status):
    self.x_position = 1
    self.y_position = 1

    self.music_station_my.start_sound('menu', 'Menu_柊キライ - ラッキー･ブルート.mp3')
    self.menu_process_flag = True
    while self.menu_process_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.music_station_my.pause('menu', 'Menu_柊キライ - ラッキー･ブルート.mp3')
                pygame.quit()
                self.music_station_my.process_flag = False
                self.menu_process_flag = False
                self.process_flag = False
            if event.type == pygame.MOUSEMOTION:
                """b_m_0"""
                if self.buttons.check_position(event, 'b_m_0'):
                    self.buttons.dictionary_of_parameters_button['b_m_0'][4] = (101, 255, 255)
                else:
                    self.buttons.dictionary_of_parameters_button['b_m_0'][4] = (51, 255, 255)
                """b_m_1"""
                if self.buttons.check_position(event, 'b_m_1'):
                    self.buttons.dictionary_of_parameters_button['b_m_1'][4] = (101, 255, 255)
                else:
                    self.buttons.dictionary_of_parameters_button['b_m_1'][4] = (51, 255, 255)
                """b_m_2"""
                if self.buttons.check_position(event, 'b_m_2'):
                    self.buttons.dictionary_of_parameters_button['b_m_2'][4] = (101, 255, 255)
                else:
                    self.buttons.dictionary_of_parameters_button['b_m_2'][4] = (51, 255, 255)
            if event.type == pygame.MOUSEBUTTONDOWN:
                """b_m_0"""
                if self.buttons.check_position(event, 'b_m_0', mobject='mouse_position + click'):
                    self.buttons.dictionary_of_parameters_button['b_m_0'][4] = (51, 255, 255)
                    self.music_station_my.pause('menu', 'Menu_柊キライ - ラッキー･ブルート.mp3')
                    self.menu_process_flag = False
                """b_m_1"""
                if self.buttons.check_position(event, 'b_m_1', mobject='mouse_position + click'):
                    self.buttons.dictionary_of_parameters_button['b_m_1'][4] = (51, 255, 255)
                    draw_setting_stage(self)
                if self.buttons.check_position(event, 'b_m_2', mobject='mouse_position + click'):
                    self.buttons.dictionary_of_parameters_button['b_m_2'][4] = (51, 255, 255)
                    self.music_station_my.pause('menu', 'Menu_柊キライ - ラッキー･ブルート.mp3')
                    pygame.quit()
                    self.music_station_my.process_flag = False
                    self.menu_process_flag = False
                    self.process_flag = False
        if not self.menu_process_flag or not self.process_flag:
            break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.music_station_my.pause('menu', 'Menu_柊キライ - ラッキー･ブルート.mp3')
        if keys[pygame.K_u]:
            self.music_station_my.unpause('menu', 'Menu_柊キライ - ラッキー･ブルート.mp3')
        if status:
            self.m_drawer.draw_game_map(self.screen, [self.player.x_position, self.player.y_position],
                                        [self.camera_x_position, self.camera_y_position], fill=self.dictionary_of_colors_core['menu_background'][0])
        else:
            self.screen.fill(self.dictionary_of_colors_core['menu_background'])
        self.buttons.draw_button(self.screen, 'b_m_0', 'Start')
        self.buttons.draw_button(self.screen, 'b_m_1', 'Settings')
        self.buttons.draw_button(self.screen, 'b_m_2', 'Exit')

        pygame.display.update()
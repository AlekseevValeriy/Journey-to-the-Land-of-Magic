
from supportiveDrawSettingStage import *
def draw_menu_stage(self, status):
    self.menu_process_flag = True
    while self.menu_process_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.menu_process_flag = False
                self.process_flag = False
            if event.type == pygame.MOUSEMOTION:
                """b_m_0"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 2 - 50, self.window_size[0] // 2 + 50,
                                       self.window_size[1] // 3 - 30, self.window_size[1] // 3 + 30):
                    self.dictionary_of_colors['b_m_0'] = (101, 255, 255)
                else:
                    self.dictionary_of_colors['b_m_0'] = (51, 255, 255)
                """b_m_1"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 2 - 50, self.window_size[0] // 2 + 50,
                                       self.window_size[1] // 2 - 30, self.window_size[1] // 2 + 30):
                    self.dictionary_of_colors['b_m_1'] = (101, 255, 255)
                else:
                    self.dictionary_of_colors['b_m_1'] = (51, 255, 255)
                """b_m_2"""
                if self.check_position(event, 'mouse_position', 'game_button_menu',
                                       self.window_size[0] // 2 - 50, self.window_size[0] // 2 + 50,
                                       self.window_size[1] // 1.5 - 30, self.window_size[1] // 1.5 + 30):
                    self.dictionary_of_colors['b_m_2'] = (101, 255, 255)
                else:
                    self.dictionary_of_colors['b_m_2'] = (51, 255, 255)
            if event.type == pygame.MOUSEBUTTONDOWN:
                """b_m_0"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 2 - 50, self.window_size[0] // 2 + 50,
                                       self.window_size[1] // 3 - 30, self.window_size[1] // 3 + 30):
                    self.dictionary_of_colors['b_m_0'] = (51, 255, 255)
                    self.menu_process_flag = False
                """b_m_1"""
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 2 - 50, self.window_size[0] // 2 + 50,
                                       self.window_size[1] // 2 - 30, self.window_size[1] // 2 + 30):
                    self.dictionary_of_colors['b_m_1'] = (51, 255, 255)
                    draw_setting_stage(self)
                if self.check_position(event, 'mouse_position + click', 'game_button_menu',
                                       self.window_size[0] // 2 - 50, self.window_size[0] // 2 + 50,
                                       self.window_size[1] // 1.5 - 30, self.window_size[1] // 1.5 + 30):
                    self.dictionary_of_colors['b_m_2'] = (51, 255, 255)
                    pygame.quit()
                    self.menu_process_flag = False
                    self.process_flag = False
        if not self.menu_process_flag or not self.process_flag:
            break
        keys = pygame.key.get_pressed()
        if status:
            self.draw_game_map(self.dictionary_of_colors['menu_background'][0])
        else:
            self.screen.fill(self.dictionary_of_colors['menu_background'])
        self.draw_button('Start', self.window_size[0] // 2 - 50, self.window_size[1] // 3 - 30, 100, 60,
                         'b_m_0', 'standart_font', self.window_size[0] // 2 - 10,
                         self.window_size[1] // 3 - 5,
                         'red')

        self.draw_button('Settings', self.window_size[0] // 2 - 50, self.window_size[1] // 2 - 30, 100, 60,
                         'b_m_1', 'standart_font', self.window_size[0] // 2 - 10,
                         self.window_size[1] // 2 - 5,
                         'red')

        self.draw_button('Exit', self.window_size[0] // 2 - 50, self.window_size[1] // 1.5 - 30, 100, 60,
                         'b_m_2', 'standart_font', self.window_size[0] // 2 - 10,
                         self.window_size[1] // 1.5 - 5,
                         'red')

        pygame.display.update()
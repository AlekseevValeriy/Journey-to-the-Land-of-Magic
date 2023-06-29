import pygame.display
from moviepy.editor import *
from supportiveDrawMenuStage import *
import parameter_reader, music_station, video_player, map_drawer, player_drawer, button_drawer

reader = parameter_reader.ParameterReader('parameter.txt')
reader.read_line([3, 5 ,7], ['window', 'game_map', 'sector'])
parameters = reader.return_parameters()

window_x_size, window_y_size = parameters['window']
map_x_size, map_y_size = parameters['game_map']
sector_x, sector_y = parameters['sector']

class GameProcess:
    def __init__(self, window_size, map_size, sector_size, quantity_of_points):
        pygame.font.init()
        pygame.display.init()
        pygame.init()

        self.window_size = window_size
        self.camera_x_position = self.window_size[0] // 2
        self.camera_y_position = self.window_size[1] // 2
        self.screen = pygame.display.set_mode((self.window_size[0], self.window_size[1]))
        self.pygame_icon = pygame.image.load('icon.bmp')
        self.full_screen_toggle = False
        pygame.display.set_caption('by Valeriy Alexeev 9A')
        pygame.display.set_icon(self.pygame_icon)

        self.music_station_my = music_station.MusicStation()
        self.music_station_my.add_sound('game', 'Game_柊キライ fea. flower - エバ.mp3', os.path.join('music', 'Game_柊キライ fea. flower - エバ.mp3'))
        self.music_station_my.add_sound('menu', 'Menu_柊キライ - ラッキー･ブルート.mp3', os.path.join('music', 'Menu_柊キライ - ラッキー･ブルート.mp3'))


        self.dictionary_of_colors_core = {'background': (255, 255, 255), 'menu_background': (102, 102, 255),
                                     'setting_background': (255, 51, 255),
                                     'red': (255, 0, 0), 'blue': (0, 0, 255), 'b_g_1': (0, 102, 51),
                                     'back': (255, 102, 0)}


        self.m_drawer = map_drawer.MapDrawer(map_size, sector_size, quantity_of_points)
        self.m_drawer.map_generate()
        self.m_drawer.color_generate()
        self.m_drawer.combine_dictionaries(self.dictionary_of_colors_core)


        self.player = player_drawer.PlayerDrawer()
        self.player.reading_sprites()
        self.FPS = 24
        self.player.choice_fps(self.FPS)


        self.buttons = button_drawer.ButtonDrawer()
        self.update_buttons()


        self.video = video_player.VideoPlayer()
        self.video.add_video("intro.mp4")
        self.video.video_start("intro.mp4")


        self.process_flag = True
        self.menu_process_flag = None
        self.setting_process_flag = None
        self.clock = pygame.time.Clock()

    def update_buttons(self):
        self.buttons.add_button('b_g_1',
                                [self.window_size[0] * 0.1, self.window_size[0] * 0.1 + 70, self.window_size[1] * 0.05,
                                 self.window_size[1] * 0.05 + 40, (0, 102, 51)])
        self.buttons.combine_colors(self.dictionary_of_colors_core)

        self.buttons.add_button('b_m_0', [self.window_size[0] // 2 - 50, self.window_size[0] // 2 + 50,
                                          self.window_size[1] // 3 - 30, self.window_size[1] // 3 + 30, (51, 255, 255),
                                          'standart_font', 'red'])
        self.buttons.add_button('b_m_1', [self.window_size[0] // 2 - 50, self.window_size[0] // 2 + 50,
                                          self.window_size[1] // 2 - 30, self.window_size[1] // 2 + 30, (51, 255, 255),
                                          'standart_font', 'red'])
        self.buttons.add_button('b_m_2', [self.window_size[0] // 2 - 50, self.window_size[0] // 2 + 50,
                                          self.window_size[1] // 1.5 - 30, self.window_size[1] // 1.5 + 30,
                                          (51, 255, 255), 'standart_font', 'red'])

        self.buttons.add_button('exp', [self.window_size[0] // 25, self.window_size[0] // 25 + 50,  self.window_size[1] // 29, self.window_size[1] // 29 + 30, 'standart_font', 'red'])
        self.buttons.add_button('b_e0',
                                [self.window_size[0] // 8, self.window_size[0] // 8 + 60, self.window_size[1] // 29,
                                 self.window_size[1] // 29 + 30, (204, 153, 102), 'standart_font', 'red'])
        self.buttons.add_button('b_e1',
                                [self.window_size[0] // 5, self.window_size[0] // 5 + 80, self.window_size[1] // 29,
                                 self.window_size[1] // 29 + 30, (204, 153, 102), 'standart_font', 'red'])
        self.buttons.add_button('b_e2',
                                [self.window_size[0] // 3.4, self.window_size[0] // 3.4 + 70, self.window_size[1] // 29,
                                 self.window_size[1] // 29 + 30, (204, 153, 102), 'standart_font', 'red'])

        self.buttons.add_button('s_m', [self.window_size[0] // 25, self.window_size[0] // 25 + 50, self.window_size[1] // 11, self.window_size[1] // 11 + 30, 'standart_font', 'red'])
        self.buttons.add_button('b_e3',
                                [self.window_size[0] // 8, self.window_size[0] // 8 + 60, self.window_size[1] // 11,
                                 self.window_size[1] // 11 + 30, (204, 153, 102), 'standart_font', 'red'])
        self.buttons.add_button('b_e4',
                                [self.window_size[0] // 5, self.window_size[0] // 5 + 80, self.window_size[1] // 11,
                                 self.window_size[1] // 11 + 30, (204, 153, 102), 'standart_font', 'red'])

        self.buttons.add_button('fps', [self.window_size[0] // 25, self.window_size[0] // 25 + 50, self.window_size[1] // 7, self.window_size[1] // 7 + 30, 'standart_font', 'red'])
        self.buttons.add_button('b_e5',
                                [self.window_size[0] // 8, self.window_size[0] // 8 + 60, self.window_size[1] // 7,
                                 self.window_size[1] // 7 + 30, (204, 153, 102), 'standart_font', 'red'])
        self.buttons.add_button('b_e6',
                                [self.window_size[0] // 5, self.window_size[0] // 5 + 80, self.window_size[1] // 7,
                                 self.window_size[1] // 7 + 30, (204, 153, 102), 'standart_font', 'red'])
        self.buttons.add_button('b_e7',
                                [self.window_size[0] // 3.4, self.window_size[0] // 3.4 + 70, self.window_size[1] // 7,
                                 self.window_size[1] // 7 + 30, (204, 153, 102), 'standart_font', 'red'])

        self.buttons.add_button('back',
                                [self.window_size[0] // 1.1, self.window_size[0] // 1.1 + 60, self.window_size[1] // 29,
                                 self.window_size[1] // 29 + 30, (255, 102, 0), 'standart_font', 'blue'])

        self.buttons.add_button('volume_s',
                                [self.window_size[0] // 25, self.window_size[0] // 25 + 50, self.window_size[1] // 5,
                                 self.window_size[1] // 5 + 30, 'standart_font', 'red'])

        self.buttons.add_button('volume', [self.window_size[0] // 8, self.window_size[0] // 3.4 + 70, self.window_size[1] // 5,
                                 self.window_size[1] // 5 + 30, (204, 153, 102)])
        self.buttons.volume_position = self.buttons.volume_position if self.window_size[0] // 8 <= self.buttons.volume_position <= self.window_size[0] // 3.4 + 70 - 30 else self.window_size[0] // 8


    def action_check(self, pygame_event):
        for event in pygame_event:
            if event.type == pygame.QUIT:
                self.music_station_my.pause('game', 'Game_柊キライ fea. flower - エバ.mp3')
                pygame.quit()
                self.process_flag = False
            if event.type == pygame.MOUSEMOTION:
                if self.buttons.check_position(event, 'b_g_1'):
                    self.dictionary_of_colors_core['b_g_1'] = (0, 152, 51)
                else:
                    self.dictionary_of_colors_core['b_g_1'] = (0, 102, 51)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons.check_position(event, 'b_g_1', mobject='mouse_position + click'):
                    self.dictionary_of_colors_core['b_g_1'] = (0, 102, 51)
                    self.music_station_my.pause('game', 'Game_柊キライ fea. flower - エバ.mp3')
                    draw_menu_stage(self, True)
                    self.music_station_my.unpause('game', 'Game_柊キライ fea. flower - エバ.mp3')
        if self.process_flag:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                self.music_station_my.pause('menu', 'Game_柊キライ fea. flower - エバ.mp3')
            if keys[pygame.K_u]:
                self.music_station_my.unpause('menu', 'Game_柊キライ fea. flower - エバ.mp3')
            if any([keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]]):
                pressed_keys = []
                for key, name in [[keys[pygame.K_a], 'K_a'], [keys[pygame.K_d], 'K_d'], [keys[pygame.K_w], 'K_w'], [keys[pygame.K_s], 'K_s']]:
                    if key:
                        pressed_keys.append(name)
                self.player.move(pressed_keys)
            if not any([keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]]):
                self.player.move(False)

    def draw_decor(self):
        pygame.draw.rect(self.screen, self.dictionary_of_colors_core['b_g_1'], (self.window_size[0] * 0.1, self.window_size[1] * 0.05, 70, 40))
        text2 = self.buttons.dictionary_of_fonts['FPS_font'].render(str(int(self.clock.get_fps())), True, self.dictionary_of_colors_core['blue'])
        self.screen.blit(text2, (50, 50))


    def core_process(self):
        value = 0
        draw_menu_stage(self, False)
        self.music_station_my.start_sound('game', 'Game_柊キライ fea. flower - エバ.mp3')
        while self.process_flag:
            self.action_check(pygame.event.get())
            if not self.process_flag:
                break
            self.m_drawer.draw_game_map(self.screen, [self.player.x_position, self.player.y_position], [self.camera_x_position, self.camera_y_position])
            value += 1
            self.player.my_animation(self.screen, [self.camera_x_position, self.camera_y_position], value)
            if value == self.player.fps // self.player.actions_in_frame:
                value = 0
            self.draw_decor()
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    game = GameProcess([window_x_size, window_y_size], [map_x_size, map_y_size], [sector_x, sector_y], [(15, 2), (10, 6), (5, 8)])
    game.core_process()

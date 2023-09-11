import pygame
from button import Button
from parameter_reader import ParameterReaderRead
from parameter_reader import ParameterReaderWrite


'''
Класс, который, получая параметры из файлов .json, создаёт экземпляры класса Button и 
визуализирует разные окна стартового меню игры, также даёт взаимодействовать с ними
'''


class StartMenu:
    def __init__(self, game_screen, clock, fps, language):
        self.clock = clock
        self.fps = fps
        self.game_screen = game_screen
        self.buttons_information = {}
        self.button_library = {}
        self.list_of_translations = ParameterReaderRead("list_of_translations.json", file_path='settings').load_parameters()
        self.process_flag = True
        self.background = pygame.image.load("textures\\title menu\\title_menu_backgorund.png")
        self.status = 'start_menu'
        self.global_language = language
        self.saves_list = []
        self.volume_flag = False
        self.refundable_world = None

    def set_buttons_information(self, name):
        self.button_library = {}
        self.buttons_information = ParameterReaderRead(name, file_path='settings').load_parameters()
        self.create_buttons()
        if self.global_language == 'ru':
            for button in self.button_library:
                old_text = self.button_library[button].text
                self.button_library[button].text = self.list_of_translations[self.status][old_text]
        if name == 'buttons_settings.json':
            self.button_library[f'button_frame_rate_{self.fps}'].texture = pygame.image.load("textures\\title menu\\buttons\\button_setting_active.png")
            self.button_library[f'button_language_{self.global_language}'].texture = pygame.image.load("textures\\title menu\\buttons\\button_setting_active.png")
        elif name == 'buttons_play.json':
            for number in range(1, 4):
                if not self.saves_list[number - 1]['saved map']:
                    self.button_library[f'button_delete_world_{number}'].enable_status = True
                    self.button_library[f'button_create_world_{number}'].enable_status = False
                    self.button_library[f'button_create_custom_world_{number}'].enable_status = False
                    self.button_library[f'button_world_{number}'].enable_status = True
                    self.button_library[f'button_delete_world_{number}'].texture = pygame.image.load("textures\\title menu\\buttons\\delete_passive.png")
                    self.button_library[f'button_create_world_{number}'].texture = pygame.image.load("textures\\title menu\\buttons\\create.png")
                    self.button_library[f'button_create_custom_world_{number}'].texture = pygame.image.load("textures\\title menu\\buttons\\create_custom.png")
                    self.button_library[f'button_world_{number}'].color_status['active'] = [48, 48, 48]

                else:
                    self.button_library[f'button_delete_world_{number}'].enable_status = False
                    self.button_library[f'button_create_world_{number}'].enable_status = True
                    self.button_library[f'button_create_custom_world_{number}'].enable_status = True
                    self.button_library[f'button_delete_world_{number}'].texture = pygame.image.load("textures\\title menu\\buttons\\delete.png")
                    self.button_library[f'button_create_world_{number}'].texture = pygame.image.load("textures\\title menu\\buttons\\create_passive.png")
                    self.button_library[f'button_create_custom_world_{number}'].texture = pygame.image.load("textures\\title menu\\buttons\\create_custom_passive.png")
                    self.button_library[f'button_world_{number}'].text = 'exist' if self.global_language == 'eng' else 'существует'

    def volume_slider_move(self, mouse_coordinate):
        if (self.button_library['volume_slider_base'].coordinate[0] + 20) > mouse_coordinate[0] - 19:
            self.button_library['volume_slider_slider'].coordinate[0] = (self.button_library['volume_slider_base'].coordinate[0] + 20)
        elif mouse_coordinate[0] - 19 > (self.button_library['volume_slider_base'].texture_size[0] + self.button_library['volume_slider_base'].coordinate[0] - 60):
            self.button_library['volume_slider_slider'].coordinate[0] = (self.button_library['volume_slider_base'].texture_size[0] + self.button_library['volume_slider_base'].coordinate[0] - 60)
        else:
            self.button_library['volume_slider_slider'].coordinate[0] = mouse_coordinate[0] - 19

    def checking_actions(self, event_outer):
        for event in event_outer:
            if event.type == pygame.QUIT:
                pygame.quit()
                self.process_flag = False
            if event.type == pygame.MOUSEMOTION:
                mouse_coordinate = event.pos
                if self.volume_flag:
                    # TODO когда-нибудь привязать его к громкости музыки, а также нужно сохранять положение кнопки после перехода между страницами
                    self.volume_slider_move(mouse_coordinate)
                for button in self.button_library:
                    button_size = self.button_library[button].texture_size
                    if (self.button_library[button].coordinate[0] <= mouse_coordinate[0] <= (self.button_library[button].coordinate[0] + button_size[0])) and (self.button_library[button].coordinate[1] <= mouse_coordinate[1] <= (self.button_library[button].coordinate[1] + button_size[1])):
                        self.button_library[button].status = 'active'
                        if button == 'volume_slider_slider':
                            self.button_library[button].texture = pygame.image.load("textures\\title menu\\buttons\\volume_active.png")
                        if ('create' in button or 'delete' in button) and not self.button_library[button].enable_status:
                            if 'custom' in button:
                                self.button_library[button].texture = pygame.image.load(f"textures\\title menu\\buttons\\{button[7:13]}_custom_active.png")
                            else:
                                self.button_library[button].texture = pygame.image.load(f"textures\\title menu\\buttons\\{button[7:13]}_active.png")
                    else:
                        if button == 'volume_slider_slider':
                            self.button_library[button].texture = pygame.image.load("textures\\title menu\\buttons\\volume.png")
                        if ('create' in button or 'delete' in button) and not self.button_library[button].enable_status:
                            if 'custom' in button:
                                self.button_library[button].texture = pygame.image.load(f"textures\\title menu\\buttons\\{button[7:13]}_custom.png")
                            else:
                                self.button_library[button].texture = pygame.image.load(f"textures\\title menu\\buttons\\{button[7:13]}.png")
                        self.button_library[button].status = 'passive'
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coordinate = event.pos
                for button in self.button_library:
                    button_size = self.button_library[button].texture_size
                    if (self.button_library[button].coordinate[0] <= mouse_coordinate[0] <= (self.button_library[button].coordinate[0] + button_size[0])) and (self.button_library[button].coordinate[1] <= mouse_coordinate[1] <= (self.button_library[button].coordinate[1] + button_size[1])) and event.button == 1:
                        if button == 'button_back':
                            self.status = 'start_menu'
                            self.set_buttons_information('buttons_start_menu.json')
                            break
                        if self.status == 'start_menu':
                            if button == 'button_play':
                                for number in range(1, 4):
                                    self.saves_list.append(ParameterReaderRead(f"saved_maps_{number}.json", file_path='maps').load_parameters())
                                self.status = 'play'
                                self.set_buttons_information('buttons_play.json')
                                break
                            elif button == 'button_setting':
                                self.status = 'settings'
                                self.set_buttons_information('buttons_settings.json')
                                break
                            elif button == 'button_credits':
                                self.status = 'credits'
                                self.set_buttons_information('buttons_credits.json')
                                break
                            elif button == 'button_exit':
                                pygame.quit()
                                self.process_flag = False
                                self.refundable_world = None
                        elif self.status == 'settings':
                            if button == 'button_frame_rate_30':
                                self.fps = 30
                                self.button_library[f'button_frame_rate_30'].texture = pygame.image.load("textures\\title menu\\buttons\\button_setting_active.png")
                                self.button_library[f'button_frame_rate_60'].texture = pygame.image.load("textures\\title menu\\buttons\\button_setting.png")
                            elif button == 'button_frame_rate_60':
                                self.fps = 60
                                self.button_library[f'button_frame_rate_60'].texture = pygame.image.load("textures\\title menu\\buttons\\button_setting_active.png")
                                self.button_library[f'button_frame_rate_30'].texture = pygame.image.load("textures\\title menu\\buttons\\button_setting.png")
                            elif button == 'button_language_ru':
                                if self.global_language != 'ru':
                                    self.global_language = 'ru'
                                    self.set_buttons_information('buttons_settings.json')
                                    break
                            elif button == 'button_language_eng':
                                if self.global_language != 'eng':
                                    self.global_language = 'eng'
                                    self.set_buttons_information('buttons_settings.json')
                                    break
                            elif button == 'volume_slider_slider':
                                self.volume_flag = True
                        elif self.status == 'play':
                            if ('create' in button and 'custom' not in button) and not self.button_library[button].enable_status:
                                # TODO добавить меню для настройки создаваемого мира
                                ParameterReaderWrite(f"saved_maps_{button[-1]}.json", ['saved map', [1]], file_path='maps').upload_parameters()
                                self.saves_list[int(button[-1]) - 1]['saved map'] = [1]
                                self.set_buttons_information('buttons_play.json')
                                break
                            elif 'delete' in button and not self.button_library[button].enable_status:
                                ParameterReaderWrite(f"saved_maps_{button[-1]}.json", ['saved map', []], file_path='maps').upload_parameters()
                                self.saves_list[int(button[-1]) - 1]['saved map'] = []
                                self.set_buttons_information('buttons_play.json')
                                break
                            elif 'button_world' in button and not self.button_library[button].enable_status:
                                # TODO добавить возможность входить и входить из миров
                                self.process_flag = False
                                self.refundable_world = int(button[-1])
                                self.status = 'start_menu'
            if event.type == pygame.MOUSEBUTTONUP:
                if self.volume_flag:
                    self.volume_flag = False

    def create_buttons(self):
        for button in self.buttons_information:
            button_inf = self.buttons_information[button]
            self.button_library[button] = Button(self.game_screen, button_inf['texture'], button_inf['font'], button_inf['font_size'], button_inf['text'], button_inf['coordinate'], button_inf['font_color_1'], button_inf['font_color_2'], button_inf['status'])

    def drawing_buttons(self):
        for button in self.button_library:
            self.button_library[button].draw_button()

    def return_data(self):
        return self.fps, self.global_language, self.refundable_world

    def menu_process(self):
        self.set_buttons_information('buttons_start_menu.json')
        while self.process_flag:
            self.game_screen.blit(self.background, (0, 0))
            self.drawing_buttons()
            self.checking_actions(pygame.event.get())
            if not self.process_flag:
                break
            pygame.display.update()
            self.clock.tick(self.fps)

    def __del__(self):
        pass

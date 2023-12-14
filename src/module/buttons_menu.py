from typing import TypeVar, Callable

from pygame import Surface, time, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame.display import update
from pygame.event import get

from button import ButtonCp, ButtonIcp, TextIcp
from json_reader import JsonReader


class ButtonsMenu:
    """Экземпляр обработки данных файла и визуализации кнопок"""
    T = TypeVar('T')

    def __init__(self, screen: Surface, clock: time.Clock, frame_rate: int, buttons_file_path: str) -> None:
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.clock = clock
        self.frame_rate = frame_rate
        self.buttons_data = self.create_buttons(JsonReader.read_file(buttons_file_path))
        self.other_data = {}
        self.buttons_binds = {}
        self.menu_process_flag = True
        self.present_menu = ''

    def add_other_data(self, **data: {T: T}) -> None:
        self.other_data = {**self.other_data, **data}

    def add_button_bind(self, **data: {str: Callable}) -> None:
        self.buttons_binds = {**self.buttons_binds, **data}

    def start_menu(self) -> None:
        """Функция для запуска процесса меню"""
        # self.present_menu = 'start_menu' # set_present_menu_name
        self.menu_process()

    def menu_process(self) -> None:
        """Функция процесса меню"""
        while self.menu_process_flag:
            self.draw_background()
            self.draw_buttons(self.present_menu)
            self.cursor_reader()
            if self.menu_process_flag:
                update()
                self.clock.tick(self.frame_rate)

    def draw_background(self) -> None:
        pass

    def draw_buttons(self, menu_name: str) -> None:
        """Функции для отрисовки кнопок"""

        def draw_button(button_name):
            self.buttons_data[menu_name][button_name].draw()

        tuple(map(draw_button, self.buttons_data[menu_name]))

    def cursor_reader(self) -> None:
        """Функция для обработки действий курсора: перемещение, нажатия"""
        for event in get():
            if event.type == QUIT:
                self.end_program()
            elif event.type == MOUSEBUTTONUP:
                buttons = self.buttons_data[self.present_menu]
                for button in buttons:
                    if event.pos in buttons[button] and not buttons[button].status == 'unactive':
                        buttons[button].status = 'active'
                    else:
                        if buttons[button].status == 'active':
                            buttons[button].status = 'passive'
            elif event.type == MOUSEBUTTONDOWN:
                pass
            elif event.type == MOUSEBUTTONUP:
                pass

    def create_buttons(self, data: dict) -> dict:
        """Функция для создания классов кнопок из информации json файла"""
        buttons = {}
        for menu_name in data:
            for button_name in data[menu_name]:
                b_d = data[menu_name][button_name]
                button_class = b_d['button_class']
                if menu_name not in buttons:
                    buttons[menu_name] = {}
                if button_class == 'button':
                    buttons[menu_name][button_name] = ButtonIcp(self.screen, texture=b_d['texture'],
                                                                status=b_d['status'], position=b_d['position'])
                elif button_class == 'text':
                    buttons[menu_name][button_name] = TextIcp(self.screen, text=b_d['text'],
                                                              font_family=b_d['font_family'],
                                                              font_size=b_d['font_size'], font_color=b_d['font_color'],
                                                              status=b_d['status'], position=b_d['position'])
                elif button_class == 'button + text':
                    buttons[menu_name][button_name] = ButtonCp(self.screen, texture=b_d['texture'], text=b_d['text'],
                                                               font_family=b_d['font_family'],
                                                               font_size=b_d['font_size'],
                                                               font_color=b_d['font_color'], status=b_d['status'],
                                                               position=b_d['position'])
        return buttons

    def end_menu(self) -> None:
        print('program registered end')
        self.menu_process_flag = False
        # exit()

    def not_found_function(self):
        print('Not found')

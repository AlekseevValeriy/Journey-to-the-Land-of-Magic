from typing import TypeVar, Callable, Any

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
        self.buttons_data, self.objects_data = self.create_buttons(JsonReader.read_file(buttons_file_path))
        self.other_data = {}
        self.buttons_binds = {}
        self.menu_process_flag = True
        self.present_menu: str = ''

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

    def draw_objects(self, menu_name):
        tuple(map(lambda object: self.objects_data[menu_name][object].draw(), self.objects_data[menu_name]))


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

    def create_buttons(self, data: dict[Any]) -> tuple[dict[dict[str, dict]], dict[dict[dict[str, dict]]]]:
        """Функция для создания классов кнопок из информации json файла"""
        buttons = {}
        objects = {}
        for menu_name in data:
            for button_name in data[menu_name]:
                button_data = data[menu_name][button_name]
                button_class_name = button_data['button_class']
                button_class_instance = None

                if button_class_name == 'button':
                    button_class_instance = ButtonIcp(self.screen, texture=button_data['texture'],
                                              status=button_data['status'],
                                              position=button_data['position'])
                elif button_class_name == 'text':
                    button_class_instance = TextIcp(self.screen, text=button_data['text'],
                                            font_family=button_data['font_family'],
                                            font_size=button_data['font_size'],
                                            font_color=button_data['font_color'],
                                            status=button_data['status'],
                                            position=button_data['position'])
                elif button_class_name == 'button + text':
                    button_class_instance = ButtonCp(self.screen, texture=button_data['texture'],
                                             text=button_data['text'],
                                             font_family=button_data['font_family'],
                                             font_size=button_data['font_size'],
                                             font_color=button_data['font_color'],
                                             status=button_data['status'],
                                             position=button_data['position'])
                if 'object' in button_name:
                    group = button_name.split('_')[1]
                    if menu_name not in objects:
                        objects[menu_name] = {}
                    if group not in objects[menu_name]:
                        objects[menu_name][group] = {}
                    objects[menu_name][group][button_name] = button_class_instance
                else:
                    if menu_name not in buttons:
                        buttons[menu_name] = {}
                    buttons[menu_name][button_name] = button_class_instance
        print(objects)
        return buttons, objects

    def create_objects(self) -> None:
        pass

    def end_menu(self) -> None:
        print('program registered end')
        self.menu_process_flag = False
        # exit()

    def not_found_function(self):
        print('Not found')

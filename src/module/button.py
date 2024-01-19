from pygame.font import Font  # pygame.font.Font imported and bound as Font
from pygame.image import load  # pygame.image.load imported and bound as load
from pygame import Surface


class ButtonMethods:
    """Класс отрисовывающий разные классы кнопок и текста"""

    def draw(self) -> None:
        """Метод отрисовывающая классы кнопок и текста"""
        class_name = self.__class__.__name__
        if class_name == 'ButtonIcp':  # отрисовка кнопки
            self.game_screen.blit(self.texture[self.status], dest=self.position, area=(0, 0, *self.size))
        elif class_name == 'TextIcp':  # отрисовка текста*
            text = self.font_family.render(self.text, True, self.font_color[self.status])
            self.game_screen.blit(text, self.position)
        elif class_name == 'ButtonCp':  # отрисовка кнопки с текстом
            self.game_screen.blit(self.texture[self.status], self.position)
            text = self.font_family.render(self.text, True, self.font_color[self.status])
            x_size, y_size = self.texture[self.status].get_size()
            text_rect = text.get_rect(center=(self.position[0] + x_size // 2,
                                              self.position[1] + y_size // 2))
            self.game_screen.blit(text, text_rect)

    def set_status(self, status: str) -> None:
        '''Метод получения статуса кнопки'''
        self.status = status

    def __contains__(self, item: list) -> bool:
        '''Магический метод проверки положения курсора в границах кнопки'''
        if all(p < i < (p + s) for i, p, s in zip(item, self.position, self.size)):
            return True
        return False


class ButtonIcp(ButtonMethods):
    """Класс кнопки"""

    def __init__(self, game_screen: Surface, **kwargs) -> None:
        self.game_screen = game_screen
        self.texture = kwargs['texture']
        for texture in self.texture:
            self.texture[texture] = load(self.texture[texture]).convert_alpha()
        self.status = kwargs['status']
        self.position = kwargs['position']
        self.size = list(self.texture[self.status].get_size())


class TextIcp(ButtonMethods):
    """Класс текста"""

    def __init__(self, game_screen: Surface, **kwargs) -> None:
        self.game_screen = game_screen
        self.text = kwargs['text']
        self.font_size = kwargs['font_size']
        self.font_family = Font(kwargs['font_family'], self.font_size)
        self.font_color = kwargs['font_color']
        self.status = kwargs['status']
        self.position = kwargs['position']
        self.size = self.font_family.render(self.text, False, 0).get_size()


class ButtonCp(ButtonMethods):
    """Класс кнопки с текстом"""

    def __init__(self, game_screen: Surface, **kwargs) -> None:
        self.game_screen = game_screen
        self.texture = kwargs['texture']
        for texture in self.texture:
            self.texture[texture] = load(self.texture[texture]).convert_alpha()
        self.text = kwargs['text']
        self.font_size = kwargs['font_size']
        self.font_family = Font(kwargs['font_family'], self.font_size)
        self.font_color = kwargs['font_color']
        self.status = kwargs['status']
        self.position = kwargs['position']
        self.size = list(self.texture[self.status].get_size())


class ButtonObject:
    '''Класс, объединяющий кнопки в один элемент'''
    def __init__(self, screen: Surface, *buttons, **data) -> None:
        self.screen = screen
        self.buttons = list(buttons)
        self.data = data

    def add_data(self, **data) -> None:
        '''Метод добавления данных в данные'''
        self.data = {**self.data, **data}

    def add_buttons(self, *buttons) -> None:
        '''Метод добавления кнопки в данные'''
        self.buttons = {*self.buttons, *buttons}

    def draw(self) -> None:
        '''Метод отрисовки кнопок'''
        for button in self.buttons:
            button.draw()

    def change_button(self, button_index: int, button) -> None:
        '''Метод смены кнопки'''
        self.buttons[button_index] = button

    def get_button(self, button_index: int):
        '''Метод получения кнопки'''
        return self.buttons[button_index]

    def change_other_data(self, data_name: str, data) -> None:
        '''Метод смены даты'''
        self.data[data_name] = data

    def get_data(self, data_name: str) -> dict:
        '''Метод получения даты'''
        return self.data[data_name]

    def get_all_data(self) -> dict:
        '''Метод получения всей даты'''
        return self.data

from pygame.font import Font # pygame.font.Font imported and bound as Font
from pygame.image import load # pygame.image.load imported and bound as load


class ButtonMethods:
    """Класс отрисовывающий разные классы кнопок и текста"""

    def draw(self) -> None:
        """Функция отрисовывающая классы кнопок и текста"""
        class_name = self.__class__.__name__
        if class_name == 'ButtonIcp':  # отрисовка кнопки
            self.game_screen.blit(self.texture[self.status], self.position)
        elif class_name == 'TextIcp':  # отрисовка текста
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
        self.status = status

    def __contains__(self, item: list) -> bool:
        if all(p < i < (p + s) for i, p, s in zip(item, self.position, self.size)):
            return True
        return False


class ButtonIcp(ButtonMethods):
    """Класс кнопки"""

    def __init__(self, game_screen, **kwargs) -> None:
        self.game_screen = game_screen
        self.texture: dict = kwargs['texture']
        for texture in self.texture:
            self.texture[texture] = load(self.texture[texture]).convert_alpha()
        self.status: str = kwargs['status']
        self.position: list = kwargs['position']
        self.size: list = self.texture[self.status].get_size()


class TextIcp(ButtonMethods):
    """Класс текста"""

    def __init__(self, game_screen, **kwargs) -> None:
        self.game_screen = game_screen
        self.text: str = kwargs['text']
        self.font_size: int = kwargs['font_size']
        self.font_family: Font = Font(kwargs['font_family'], self.font_size)
        self.font_color: dict = kwargs['font_color']
        self.status: str = kwargs['status']
        self.position: list = kwargs['position']
        self.size: tuple = self.font_family.render(self.text, False, 0).get_size()


class ButtonCp(ButtonMethods):
    """Класс кнопки с текстом"""

    def __init__(self, game_screen, **kwargs) -> None:
        self.game_screen = game_screen
        self.texture: dict = kwargs['texture']
        for texture in self.texture:
            self.texture[texture] = load(self.texture[texture]).convert_alpha()
        self.text: str = kwargs['text']
        self.font_size: int = kwargs['font_size']
        self.font_family: Font = Font(kwargs['font_family'], self.font_size)
        self.font_color: dict = kwargs['font_color']
        self.status: str = kwargs['status']
        self.position: list = kwargs['position']
        self.size: list = self.texture[self.status].get_size()

class ButtonObject:
    def __init__(self, screen, *buttons, **data):
        self.screen = screen
        self.buttons = list(buttons)
        self.data = data

    def draw(self):
        for button in self.buttons:
            button.draw()

    def change_button(self, button_index, button):
        self.buttons[button_index] = button

    def get_button(self, button_index):
        return self.buttons[button_index]

    def change_other_data(self, data_name, data):
        self.data[data_name] = data

    def get_data(self, data_name):
        return self.data[data_name]

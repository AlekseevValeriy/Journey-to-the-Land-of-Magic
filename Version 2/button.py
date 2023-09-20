import pygame


"""
Класс, который хранит все параметры кнопки.
Параметры берутся из файлов .json
"""


class Button:
    def __init__(self, game_screen, texture, font, font_size, text, coordinate, font_color_passive, font_color_active, color_status, enable_status=False):
        self.game_screen = game_screen
        self.texture = pygame.image.load(texture).convert_alpha()
        self.texture_size = self.texture.get_size()
        pygame.font.init()
        self.font = pygame.font.Font(font, font_size)
        self.text = text
        self.coordinate = coordinate
        self.color_status = {"active": font_color_active, "passive": font_color_passive}
        self.status = color_status
        self.enable_status = enable_status

    def draw_button(self):
        self.game_screen.blit(self.texture, self.coordinate)
        if self.text != 'None':
            button_text = self.font.render(self.text, True, self.color_status[self.status])
            button_text_rect = button_text.get_rect(center=(self.coordinate[0] + self.texture_size[0] // 2, self.coordinate[1] + self.texture_size[1] // 2))
            self.game_screen.blit(button_text, button_text_rect)

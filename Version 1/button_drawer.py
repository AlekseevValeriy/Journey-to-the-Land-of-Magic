import pygame

class ButtonDrawer:
    def __init__(self):
        self.dictionary_of_fonts = {'standart_font': pygame.font.SysFont('Insight Sans SSi', 18),
                                    'FPS_font': pygame.font.Font('fonts/Samson.ttf', 50)}
        self.dictionary_of_colors_button = {}
        self.dictionary_of_parameters_button = {}

        for n in range(3):
            self.dictionary_of_colors_button[f'b_m_{n}'] = (51, 255, 255)
        for n in range(8):
            self.dictionary_of_colors_button[f'b_e{n}'] = (204, 153, 102)
        self.volume_position = 0
        self.last_position = 0

    def add_color(self, color_name, color, many=False):
        if many:
            for name, color_n in zip(color_name, color):
                self.dictionary_of_parameters_button[name] = color_n
            return
        self.dictionary_of_parameters_button[color_name] = color

    def add_font(self, font_name, font, many=False):
        if many:
            for name, font_n in zip(font_name, font):
                self.dictionary_of_parameters_button[name] = font_n
            return
        self.dictionary_of_parameters_button[font_name] = font

    def add_button(self, button_name, button_parameter, many=False):
        #  button_parameter(with button) = [0, 0, 0, 0, (0, 0, 0), 'font', (0, 0, 0)]
        #  or
        #  button_parameter(without button) = [0, 0, 0, 0, 'font', (0, 0, 0)]
        #  or
        #  button_parameter(without text) = [0, 0, 0, 0, (0, 0, 0)]
        if many:
            for name, parameter in zip(button_name, button_parameter):
                self.dictionary_of_parameters_button[name] = parameter
            return
        self.dictionary_of_parameters_button[button_name] = button_parameter

    def combine_colors(self, other_dict):
        for color in other_dict:
            self.dictionary_of_colors_button[color] = other_dict[color]


    def check_position(self, pygame_event, button_name, mobject='mouse_position'):
        position = pygame_event.pos
        button_parameter = self.dictionary_of_parameters_button[button_name]
        if button_parameter[0] <= position[0] <= button_parameter[1] and\
                button_parameter[2] <= position[1] <= button_parameter[3]:
            if mobject == 'mouse_position + click' and pygame_event.button == 1:
                return True
            elif mobject == 'mouse_position':
                return True
            elif mobject == 'mouse_position + press' and pygame_event.button == 1:
                print(position[0], self.last_position)
                self.volume_position = position[0] if button_parameter[0] <= position[0] <= button_parameter[1] - 30 else button_parameter[1] - 30
                return True
        return False


    def draw_button(self, game_screen, button_name, text):
        button_parameter = self.dictionary_of_parameters_button[button_name]
        width = button_parameter[1] - button_parameter[0]
        hight = button_parameter[3] - button_parameter[2]
        if len(button_parameter) == 7:
            pygame.draw.rect(game_screen, button_parameter[4], (button_parameter[0], button_parameter[2], width, hight))
            button_text = self.dictionary_of_fonts[button_parameter[5]].render(text, True, button_parameter[6])
            button_text_rect = button_text.get_rect(center=(button_parameter[0] + width // 2, button_parameter[2] + hight // 2))
            game_screen.blit(button_text, button_text_rect)
        elif len(button_parameter) == 6:
            button_text = self.dictionary_of_fonts[button_parameter[4]].render(text, True, button_parameter[5])
            button_text_rect = button_text.get_rect(center=(button_parameter[0] + width // 2, button_parameter[2] + hight // 2))
            game_screen.blit(button_text, button_text_rect)
        elif len(button_parameter) == 5:
            pygame.draw.rect(game_screen, button_parameter[4], (button_parameter[0], button_parameter[2], width, hight))

    def draw_special_button_volume(self, game_screen, button_name):
        button_parameter = self.dictionary_of_parameters_button[button_name]
        width = button_parameter[1] - button_parameter[0]
        hight = button_parameter[3] - button_parameter[2]
        pygame.draw.rect(game_screen, button_parameter[4], (button_parameter[0], button_parameter[2], width, hight))
        pygame.draw.rect(game_screen, [n - 10 for n in button_parameter[4]], (self.volume_position, button_parameter[2], hight, hight))

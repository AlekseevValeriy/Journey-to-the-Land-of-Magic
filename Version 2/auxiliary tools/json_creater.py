import json
import os
import pygame

pygame.display.init()


def create_buttons(file_name, times):
    with open(file_name, 'r') as file:
        buttons = json.load(file)
    # for _ in range(times):
    #     print(f'button {_}')
    #     name = input('name  ')
    #     texture = input('texture  ')
    #     text = input('text  ')
    #     coordinate = [int(i) for i in input('coordinate  ').split()]
    #     font_color_1 = [int(i) for i in input('font color 1  ').split()]
    #     font_color_2 = [int(i) for i in input('font color 2  ').split()]
    #     font_size = int(input('font size  '))
    #     print()
    #     data = {"texture": texture, "font": "fonts\\Book Antiqua.ttf", "text": text, "coordinate": coordinate, "font_color_1": font_color_1, "font_color_2": font_color_2, "font_size": font_size, "status": "passive"}
    #     buttons[name] = data

    for button in buttons:
        print(buttons[button]['text'])
        # buttons[button]['texture'] = os.path.join('textures', 'title menu', 'buttons', 'button.png')
        # buttons[button]['font_color_1'] = [48, 48, 48]
        # buttons[button]['font_color_2'] = [96, 96, 96]
        # buttons[button]['font'] = os.path.join('fonts', 'Book Antiqua.ttf')
        # buttons[button]['font_size'] = 20
        # buttons[button]['coordinate'] = [777, 540]
        # buttons[button]['status'] = 'passive'
        # buttons[button]['font'] = "fonts\\Book Antiqua.ttf"

    with open(file_name, 'w') as file:
        json.dump(buttons, file)

create_buttons('../settings/buttons_start_menu.json', 11)
# def a(*args):
#     for i, j in args:
#         print(f'{i} - {j}')
#
# a([1, 2], ['a', 'b'], ['www', 1])
# import pygame
#
# pygame.init()
# pygame.event.set_blocked(None)
# pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
#                           pygame.MOUSEWHEEL, pygame.KEYUP, pygame.KEYDOWN])
#
# screen = pygame.display.set_mode((640, 480))
#
# while True:
#     for o in pygame.event.get():
#         if o.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
#             print(o.pos)
# print(bool(None))
text = {
    "buttons_credits": {"back": "назад", "credits": "заслуги", "Journey to the Land of Magic": "Путешествие в страну волшебства", "Developed": "разработано", "Valeriy E. A.": "Валерий Е. А.", "Game design": "Игровой дизайн", "------": "------", "Programming": "Запрограммировано"},
    "buttons_settings": {"back": "назад", "settings": "настройки", "volume": "громкость", "None": "None", "frame rate": "частота смены кадров", "30": "30", "60": "60", "language": "язык", "ru": "рус", "eng": "англ"},
    "buttons_start_menu": {"play": "играть", "setting": "настройки", "credits": "заслуги", "exit": "выход", "Journey to the Land of Magic": "Путешествие в страну волшебства"}
}
import json

# with open('list_of_translations.json', 'w') as file:
#     json.dump(text, file)

with open('../settings/list_of_translations.json', 'r') as file:
    data = json.load(file)

for i in data:
    print(data[i])
import pygame

from game_process import GameProcess
from parameter_reader import ParameterReaderRead
from start_menu import StartMenu
from world_generator import WorldGenerator

""""
Класс, который обобщает все остальные классы и показывает результат в окне pygame
"""


class PygameWindow:
    def __init__(self):
        pygame.init()
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
                                  pygame.MOUSEWHEEL, pygame.KEYUP, pygame.KEYDOWN])
        self.settings = ParameterReaderRead('game_settings.json', file_path='settings').load_parameters()
        self.screen = pygame.display.set_mode(self.settings['screen_resolution'], pygame.FULLSCREEN, pygame.DOUBLEBUF)
        self.fps = self.settings['frame_rate']
        self.clock = pygame.time.Clock()
        self.global_language = 'eng'
        self.game_all_game = True
        self.selected_world = None

    def all_game_process(self):
        menu = StartMenu(self.screen, self.clock, self.fps, self.global_language)
        menu.create_buttons()
        while self.game_all_game:
            menu.menu_process()
            self.fps, self.global_language, self.selected_world = menu.return_data()
            if self.selected_world:
                world = WorldGenerator(400, 400)
                world.create_world_layout(regions=[2, 3, 4, 5])
                player_coordinate = world.make_player_coordinate()
                world.create_world()
                world = world.return_world_layout()
                gaming_process = GameProcess(self.screen, self.fps, self.clock, self.global_language, world, player_coordinate)
                gaming_process.game_process()
                menu.process_flag = True
            else:
                break


if __name__ == '__main__':
    game = PygameWindow()
    game.all_game_process()

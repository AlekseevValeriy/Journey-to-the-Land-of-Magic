import pygame
from parameter_reader import ParameterReaderRead
from start_menu import StartMenu
from game_process import GameProcess
from world_generator_2 import WorldGenerator


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
                # TODO сделать игровой процесс
                world = WorldGenerator(100, 100, sector_size=16)
                world.create_world_layout()
                world.create_world()
                world = world.return_world_layout()
                game = GameProcess(self.screen, self.fps, self.clock, self.global_language, world, [0, 0])
                game.game_process()
                menu.process_flag = True
            else:
                break


if __name__ == '__main__':
    game = PygameWindow()
    game.all_game_process()

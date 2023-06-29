import pygame
from parameter_reader import ParameterReaderRead
from start_menu import StartMenu


class PygameWindow:
    def __init__(self):
        pygame.init()
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
                                  pygame.MOUSEWHEEL, pygame.KEYUP, pygame.KEYDOWN])
        settings = ParameterReaderRead('game_settings.json', file_path='settings').load_parameters()
        self.screen = pygame.display.set_mode(settings['screen_resolution'], pygame.FULLSCREEN, pygame.DOUBLEBUF)
        self.fps = settings['frame_rate']
        self.clock = pygame.time.Clock()
        self.global_language = 'eng'

    def game_process(self):
        menu = StartMenu(self.screen, self.clock, self.fps)
        menu.create_buttons()
        menu.menu_process()
        self.fps, self.global_language = menu.return_data()


if __name__ == '__main__':
    game = PygameWindow()
    game.game_process()

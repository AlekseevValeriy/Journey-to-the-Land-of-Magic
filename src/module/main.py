from pygame import init as pg_init
from pygame.time import Clock
from pygame.display import set_mode as pg_window
from start_buttons_menu import StartButtonsMenu
from json_reader import JsonReader
from screen_effect import ScreenEffect

class Main:
    def __init__(self):
        pg_init()
        settings_data = JsonReader.read_file('../../data/json/settings_data.json')
        self.SCREEN_SIZE = settings_data['settings_data']
        self.frame_rate = settings_data['frame_rate']
        self.player = 'player'
        self.clock = Clock()
        self.screen = pg_window(self.SCREEN_SIZE)

    def run(self):
        # ScreenEffect(self.screen, self.clock, self.frame_rate).game_intro()
        game_menu = StartButtonsMenu(self.screen, self.clock, self.frame_rate,
                                     '../../data/json/start_buttons_data.json')
        game_menu.start_menu()

if __name__ == '__main__':
    game = Main()
    game.run()

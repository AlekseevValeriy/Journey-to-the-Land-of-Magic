from sys import exit

from pygame import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, KEYDOWN, KEYUP
from pygame.display import update
from pygame.event import get

from buttons_menu import ButtonsMenu
from player import Player
from world import World
from button import ButtonObject


class GameButtonsMenu(ButtonsMenu):
    def __init__(self, screen, clock, frame_rate, buttons_file_path, world, person: str, position: list):
        super().__init__(screen=screen, clock=clock, frame_rate=frame_rate, buttons_file_path=buttons_file_path)
        self.add_other_data(move=False)
        self.add_button_bind(back_button=self.end_menu)
        self.keys_dict = {1073741903: 'right', 1073741904: 'left', 1073741906: 'up', 1073741905: 'down'}
        self.world = World(screen, world)
        self.player = Player(screen, position, person)
        self.player.change_step_under_frame_rate(self.frame_rate)
        self.button_objects = {}
        self.create_button_objects()

    def create_button_objects(self):
        # процесс сбора нужных objects в ButtonObject и настройка данных
        # написать в json gAMES BUTTONS кнопки и составить из них объекты, возможно новые отдельные классы
        pass

    def start_menu(self) -> None:
        self.present_menu = 'game_menu'
        self.menu_process()

    def menu_process(self) -> None:
        while self.menu_process_flag:
            self.draw_background()
            self.game_unit()
            self.draw_buttons(self.present_menu)
            if self.menu_process_flag:
                update()
                self.clock.tick(self.frame_rate)

    def game_unit(self) -> None:
        self.screen.fill('white')
        self.world.draw_world(self.player.get_position())
        self.player.draw_player()
        self.cursor_reader()

    def cursor_reader(self) -> None:
        for event in get():
            if event.type == QUIT:
                self.menu_process_flag = False
                exit()
            elif event.type == KEYDOWN:
                if self.keys_dict.get(event.key, False):
                    self.run_action(self.keys_dict[event.key])
            elif event.type == KEYUP:
                if self.keys_dict.get(event.key, False):
                    self.stand_action()


            elif event.type == MOUSEMOTION:
                buttons = self.buttons_data[self.present_menu]
                for button in buttons:
                    if event.pos in buttons[button] and not buttons[button].status == 'unactive':
                        buttons[button].status = 'active'
                    else:
                        if buttons[button].status == 'active':
                            buttons[button].status = 'passive'
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons = self.buttons_data[self.present_menu]
                    for button in buttons:
                        if event.pos in buttons[button]:
                            self.buttons_binds.get(button, self.not_found_function)()
            elif event.type == MOUSEBUTTONUP:
                pass

        if self.other_data['move']:
            self.player.player_move('run')
        else:
            self.player.player_move('stand')

    def run_action(self, side):
        self.other_data['move'] = True
        self.player.set_face_side(side)

    def stand_action(self):
        self.other_data['move'] = False

    def end_menu(self) -> None:
        self.menu_process_flag = False
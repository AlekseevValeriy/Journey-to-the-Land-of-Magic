import pygame

from buttons_menu import ButtonsMenu
from pygame.image import load
from pygame.font import SysFont
from pygame import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.event import get

from sys import exit


class Battle(ButtonsMenu):
    def __init__(self, screen, clock, frame_rate, buttons_file_path):
        super().__init__(screen=screen, clock=clock, frame_rate=frame_rate, buttons_file_path=buttons_file_path)
        self.add_other_data(background=load("../../data/textures/backgrounds/battle_background.png").convert_alpha(),
                            fps_counter=True, fps_font=SysFont('Comic Sans MS', 30))
        self.add_button_bind(back_to_game=self.end_program)
        self.player: Attendee
        self.enemy: Attendee

    def start_battle(self, player_data, enemy_data):
        self.player = Attendee(player_data, self.screen, self.clock, self.frame_rate)
        self.enemy = Attendee(enemy_data, self.screen, self.clock, self.frame_rate)

    def end_battle(self):
        self.player = None
        self.enemy = None
        self.menu_process_flag = True

    def start_menu(self, player_data: dict, enemy_data: dict) -> None:
        self.present_menu = 'battle_menu'
        self.start_battle(player_data, enemy_data)
        self.menu_process()
        self.end_battle()

    def draw_background(self) -> None:
        self.screen.blit(self.other_data['background'], (0, 0))

    def draw_fps(self):
        if self.other_data['fps_counter']:
            text = self.other_data['fps_font'].render(str(int(self.clock.get_fps())), True, 'gray')
            self.screen.blit(text, (1879, 5))

    def draw_scene(self):
        self.player.draw()
        self.enemy.draw()

    def cursor_reader(self) -> None:
        for event in get():
            if event.type == QUIT:
                self.end_program()
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
                            if not buttons[button].status == 'unactive':
                                self.buttons_binds.get(button, self.not_found_function)()
            elif event.type == MOUSEBUTTONUP:
                pass

    def menu_process(self) -> None:
        while self.menu_process_flag:
            self.draw_background()
            self.draw_scene()
            self.draw_buttons(self.present_menu)
            self.draw_objects(self.present_menu)
            self.cursor_reader()
            self.draw_fps()
            if self.menu_process_flag:
                pygame.display.update()
                self.clock.tick(self.frame_rate)

    # ---------сектор действий кнопок меню---------

    def end_program(self):
        print('program registered end')
        self.menu_process_flag = False

    def not_found_function(self):
        print('Not found')


class Attendee:
    def __init__(self, characteristics: dict, *base: tuple[pygame.Surface, pygame.time.Clock, int], ):
        self.screen = base[0]
        self.clock = base[1]
        self.frame_rate = base[2]
        self.characteristics = characteristics
        if type(self.characteristics['texture']) is str:
            self.texture = pygame.image.load(self.characteristics['texture']).convert_alpha()
        elif type(self.characteristics['texture']) is pygame.Surface:
            self.texture = self.characteristics['texture']
        self.side = self.characteristics['side']
        self.position = [0, 540 - self.texture.get_height() // 2]
        if self.side == 'left':
            self.position[0] = 150
        elif self.side == 'right':
            self.position[0] = 1920 - 150 - self.texture.get_width()

    def draw(self):
        self.screen.blit(self.texture, self.position)

    def is_alive(self):
        if self.characteristics['hp'] <= 0:
            return True
        return False

from sys import exit

from pygame import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, KEYDOWN, KEYUP, K_x
from pygame.display import update
from pygame.event import get

from buttons_menu import ButtonsMenu
from player import Player
from world import World
from custom_object_buttons import StatusBar, WorldMap


class GameButtonsMenu(ButtonsMenu):
    def __init__(self, screen, clock, frame_rate, buttons_file_path, sample_world=None):
        super().__init__(screen=screen, clock=clock, frame_rate=frame_rate, buttons_file_path=buttons_file_path)
        self.add_other_data(move=False)
        self.add_button_bind(back_button=self.end_menu)
        self.keys_dict = {1073741903: 'right', 1073741904: 'left', 1073741906: 'up', 1073741905: 'down'}
        self.world = None
        self.player = None
        self.sample_world = sample_world
        self.create_button_objects()

    def create_button_objects(self):
        objects_sb = self.objects_data['game_menu']['sb']
        self.objects_data['game_menu']['sb'] = StatusBar(self.screen,
                                                            *tuple(map(lambda name: objects_sb[name], objects_sb)))
        objects_mp = self.objects_data['game_menu']['mp']
        self.objects_data['game_menu']['mp'] = WorldMap(self.screen,
                                                         *tuple(map(lambda name: objects_mp[name], objects_mp)))


    def create_world(self, world):
        self.world = World(self.screen, world)

    def create_player(self, person, position):
        self.player =  Player(self.screen, position, person)

    def start_menu(self) -> None:
        self.objects_data['game_menu']['mp'].set_world_map(self.sample_world)
        self.objects_data['game_menu']['sb'].born()
        self.player.change_step_under_frame_rate(self.frame_rate)
        self.menu_process_flag = True
        self.present_menu = 'game_menu'
        self.menu_process()

    def menu_process(self) -> None:
        while self.menu_process_flag:
            self.draw_background()
            self.game_unit()
            self.draw_buttons(self.present_menu)
            self.draw_objects(self.present_menu)
            self.objects_data['game_menu']['sb'].dead_check()
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
            elif event.type == KEYDOWN and self.objects_data['game_menu']['sb'].get_persona_status():
                if self.keys_dict.get(event.key, False):
                    self.objects_data['game_menu']['mp'].set_player_position(self.player.get_position())
                    self.run_action(self.keys_dict[event.key])
                if event.key == K_x:
                    print('x')
                    self.objects_data['game_menu']['sb'].reduce_parameter('hp', 10)
            elif event.type == KEYUP:
                if self.keys_dict.get(event.key, False) or not self.objects_data['game_menu']['sb'].get_persona_status():
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
        self.other_data['move'] = False
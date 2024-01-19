from random import choice, randint
from threading import Thread, Semaphore

import pygame

from buttons_menu import ButtonsMenu
from json_reader import JsonReader
from music_manager import MusicManager
from screen_effect import ScreenEffect

from typing import Callable

general_semaphore = Semaphore(1)

def order_for_queue(function: Callable):
    '''Декоратор для работы очереди потоков'''
    def order(self, *args, **kwargs):
        general_semaphore.acquire()
        function(self, *args, **kwargs)
        general_semaphore.release()
    return order


class Battle(ButtonsMenu):
    '''Класс процесса Битвы'''
    def __init__(self, screen: pygame.Surface, clock:pygame.time.Clock, frame_rate: int, buttons_file_path: str) -> None:
        super().__init__(screen=screen, clock=clock, frame_rate=frame_rate, buttons_file_path=buttons_file_path)
        self.add_other_data(background=pygame.image.load("../../data/textures/backgrounds/battle_background.png").convert_alpha(),
                            fps_counter=True, fps_font=pygame.font.SysFont('Comic Sans MS', 30), queue=BattleQueue(),
                            bar_size=self.buttons_data['battle_menu']['hp_bar_right'].size[0], battle_exp=0,
                            ending_data=None, screen_effect=ScreenEffect(self.screen, self.clock, frame_rate),
                            music_manager=MusicManager(0.5))
        self.add_button_bind(run_button_left=self.end_battle_process,
                             attack_button_left=self.player_attack_move,
                             magic_button_left=self.player_magic_move)
        self.player: Attendee
        self.enemy: Attendee

    def click_sound(function: Callable):
        '''Декоратор для добавления звука, при нажатии на кнопки'''
        def click(self, *args, **kwargs):
            function(self, *args, **kwargs)
            self.other_data['music_manager'].activate_effect('click')
        return click

    def start_battle(self, player_data: dict, enemy_data: dict) -> None:
        '''Метод для настройки и начала процесса битвы'''
        value = (JsonReader.read_file('../../data/json/settings_data.json')['volume_trigger_position'] - 816) * 100 // (
                    1100 - 816) / 100
        if value > 1:
            value = 1
        if value < 0:
            value = 0
        self.other_data['music_manager'].set_volume(value)
        self.other_data['music_manager'].activate_music('cool_piano')
        self.player = Attendee(self.other_data['music_manager'], player_data, self.screen, self.clock, self.frame_rate)
        enemy_data['level'] = player_data['level']
        enemy_data['fb_level'] = player_data['fb_level']
        self.enemy = Attendee(self.other_data['music_manager'], enemy_data, self.screen, self.clock, self.frame_rate)
        self.update_visual_queue()

    def end_battle(self) -> None:
        '''Метод для настройки и окончания процесса битвы'''
        self.other_data['music_manager'].stop_sound('all')
        self.player = None
        self.enemy = None
        self.menu_process_flag = True

    def start_menu(self, player_data: dict, enemy_data: dict) -> None:
        '''Метод начала битвы'''
        self.present_menu = 'battle_menu'
        self.start_battle(player_data, enemy_data)
        self.menu_process()
        self.end_battle()

    def draw_background(self) -> None:
        '''Метод отрисовки заднего фона'''
        self.screen.blit(self.other_data['background'], (0, 0))

    def draw_fps(self) -> None:
        '''Метод отрисовки счётчика fps'''
        if self.other_data['fps_counter']:
            text = self.other_data['fps_font'].render(str(int(self.clock.get_fps())), True, 'gray')
            self.screen.blit(text, (1879, 5))

    def draw_scene(self) -> None:
        '''Метод рисования сущностей'''
        self.player.draw()
        self.enemy.draw()

    def cursor_reader(self) -> None:
        '''Метод обработки действий'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end_battle()
            elif event.type == pygame.MOUSEMOTION:
                buttons = self.buttons_data[self.present_menu]
                for button in buttons:
                    if event.pos in buttons[button] and not buttons[button].status == 'unactive':
                        if button not in ['turn', 'attack_button_right', 'magic_button_right', 'run_button_right']:
                            buttons[button].status = 'active'
                    else:
                        if buttons[button].status == 'active':
                            buttons[button].status = 'passive'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    buttons = self.buttons_data[self.present_menu]
                    for button in buttons:
                        if event.pos in buttons[button]:
                            if not buttons[button].status == 'unactive':
                                if button not in ['turn', 'attack_button_right', 'magic_button_right',
                                                  'run_button_right']:
                                    self.buttons_binds.get(button, self.not_found_function)()
            elif event.type == pygame.MOUSEBUTTONUP:
                pass

    def menu_process(self) -> None:
        '''Метод процесса меню'''
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

    @click_sound
    def end_battle_process(self) -> None:
        '''Метод выхода из меню битвы'''
        # print('battle registered end')
        self.menu_process_flag = False
        self.ending_characteristics()

    def not_found_function(self) -> None:
        '''Метод для уведомления об отсутствии действия у кнопки'''
        # print('Not found')
        pass

    def update_visual_queue(self) -> None:
        '''Метод очереди ходов у сущностей'''
        if not self.other_data['queue'].get_present_queue():
            self.buttons_data['battle_menu']['attack_button_right'].status = 'unactive'
            self.buttons_data['battle_menu']['magic_button_right'].status = 'unactive'
            self.buttons_data['battle_menu']['run_button_right'].status = 'unactive'
            self.buttons_data['battle_menu']['attack_button_left'].status = 'passive'
            if self.player.characteristics['fb_level'] == 0 or self.player.characteristics['mp'] <= 0:
                self.buttons_data['battle_menu']['magic_button_left'].status = 'unactive'
            else:
                self.buttons_data['battle_menu']['magic_button_left'].status = 'passive'
            self.buttons_data['battle_menu']['run_button_left'].status = 'passive'
            self.buttons_data['battle_menu']['turn'].status = 'passive'
        else:
            self.buttons_data['battle_menu']['attack_button_right'].status = 'passive'
            if self.enemy.characteristics['fb_level'] == 0 or self.enemy.characteristics['mp'] <= 0:
                self.buttons_data['battle_menu']['magic_button_right'].status = 'unactive'
            else:
                self.buttons_data['battle_menu']['magic_button_right'].status = 'passive'
            self.buttons_data['battle_menu']['run_button_right'].status = 'passive'
            self.buttons_data['battle_menu']['attack_button_left'].status = 'unactive'
            self.buttons_data['battle_menu']['magic_button_left'].status = 'unactive'
            self.buttons_data['battle_menu']['run_button_left'].status = 'unactive'
            self.buttons_data['battle_menu']['turn'].status = 'unactive'
        self.buttons_data['battle_menu']['hp_bar_left'].size[0] = self.player.get_hp_percent() * self.other_data[
            'bar_size']
        self.buttons_data['battle_menu']['mp_bar_left'].size[0] = self.player.get_mp_percent() * self.other_data[
            'bar_size']
        self.buttons_data['battle_menu']['hp_bar_right'].size[0] = self.enemy.get_hp_percent() * self.other_data[
            'bar_size']
        self.buttons_data['battle_menu']['mp_bar_right'].size[0] = self.enemy.get_mp_percent() * self.other_data[
            'bar_size']

    @click_sound
    def player_attack_move(self) -> None:
        '''Метод атаки игрока'''
        self.player_turn('attack')

    @click_sound
    def player_magic_move(self) -> None:
        '''Метод магии игрока'''
        self.player_turn('magic')

    def player_turn(self, move) -> None:
        '''Метод хода игрока'''
        self.player.move_animation(move)
        self.enemy.get_damage(self.player.set_damage(move))
        if not self.enemy.is_alive():
            self.add_exp(self.player.characteristics['level'])
            self.ending_characteristics()
            Thread(target=self.long_end_battle_process, daemon=True).start()
            self.other_data['screen_effect'].battle_end_animation('win')
        else:
            self.other_data['queue'].change_queue()
            self.update_visual_queue()
            Thread(target=self.enemy_turn).start()

    @order_for_queue
    def enemy_turn(self) -> None:
        '''Метод хода противника'''
        self.my_sleep()
        if self.enemy.characteristics['fb_level'] > 0:
            move = choice(('attack', 'magic'))
        else:
            move = 'attack'
        self.enemy.move_animation(move)
        self.player.get_damage(self.enemy.set_damage(move))
        if not self.player.is_alive():
            self.reduce_exp(self.player.characteristics['level'])
            self.ending_characteristics()
            self.other_data['screen_effect'].battle_end_animation('Lose')
            Thread(target=self.long_end_battle_process, daemon=True).start()
        else:
            self.other_data['queue'].change_queue()
            self.update_visual_queue()

    def my_sleep(self) -> None:
        '''Метод остановки времени'''
        pygame.time.delay(1000)

    @order_for_queue
    def long_end_battle_process(self) -> None:
        '''Метод выхода из меню битвы с анимацией'''
        self.update_visual_queue()
        self.my_sleep()
        self.end_battle_process()

    def add_exp(self, level: int) -> None:
        '''Метод добавления опыта игроку'''
        self.other_data['battle_exp'] += self.get_exp(level)

    def reduce_exp(self, level: int) -> None:
        '''Метод уменьшения опыта у игрока'''
        self.other_data['battle_exp'] -= self.get_exp(level)

    def get_exp(self, level=1) -> int:
        '''Метод получения количества опыта'''
        return 10 * level

    def ending_characteristics(self) -> None:
        '''Метод получения характеристик'''
        self.other_data['ending_data'] = {'hp': self.player.characteristics['hp'],
                'mp': self.player.characteristics['mp'],
                'exp': self.other_data['battle_exp']}

    def get_ending_data(self) -> None:
        '''Метод получения данных после битвы'''
        return self.other_data['ending_data']



class Attendee:
    '''Метод сущности'''
    def __init__(self, music_manager: MusicManager,  characteristics: dict, *base: tuple[pygame.Surface, pygame.time.Clock, int]) -> None:
        self.music_manager = music_manager
        self.screen = base[0]
        self.clock = base[1]
        self.frame_rate = base[2]
        self.characteristics = characteristics
        if 'str' not in self.characteristics:
            points = self.characteristics['level']
            str_points = randint(1, points)
            self.characteristics['str'] = str_points
            points -= str_points
            if points:
                dex_points = randint(1, points)
            else:
                dex_points = 0
            self.characteristics['dex'] = dex_points
            points -= dex_points
            self.characteristics['int'] = points
            self.characteristics['fb_level'] = randint(0, self.characteristics['level'])
            self.characteristics['hp'] = self.characteristics['max_hp'] = 200 * (1.2 ** self.characteristics['level'])
            self.characteristics['mp'] = self.characteristics['max_mp'] = 100 * (1.1 ** self.characteristics['level'])
        if type(self.characteristics['texture']) is str:
            self.texture = pygame.image.load(self.characteristics['texture']).convert_alpha()
        elif type(self.characteristics['texture']) is pygame.Surface:
            self.texture = self.characteristics['texture']
        self.side = self.characteristics['side']
        self.position = [0, 540 - self.texture.get_height() // 2]
        self.fireball = pygame.image.load("..//..//data//textures//magic//fireball.png").convert_alpha()
        if self.side == 'left':
            self.position[0] = 150
            self.steps = [15, 3, 3, 15, 15]
            self.ends = [1920 - 150 - 75, 1920 - 150 - 50, 1920 - 150 - 75, 150, 1920 - 150 - 50]
        elif self.side == 'right':
            self.fireball = pygame.transform.flip(self.fireball, True, False)
            self.position[0] = 1920 - 150 - self.texture.get_width()
            self.steps = [-15, -3, -3, -15, -15]
            self.ends = [150 + 75, 150 + 50, 150 + 75, 1920 - 150 - self.texture.get_width(), 150 + 50]

    def draw(self) -> None:
        '''Метод отрисовки сущности'''
        self.screen.blit(self.texture, self.position)

    def is_alive(self) -> bool:
        '''Метод проверки жизни сущности'''
        if self.characteristics['hp'] <= 0:
            return False
        return True

    def move_animation(self, move: str) -> None:
        '''Метод анимации действия сущности'''
        if move == 'attack':
            Thread(target=self.attack_animation, daemon=True).start()
        elif move == 'magic':
            Thread(target=self.magic_animation, daemon=True).start()

    @order_for_queue
    def attack_animation(self) -> None:
        '''Метод анимации атаки'''
        if self.side == 'left':
            while self.position[0] <= self.ends[0]:
                self.position[0] += self.steps[0]
                pygame.time.delay(3)

            while self.position[0] <= self.ends[1]:
                self.position[0] += self.steps[1]
                pygame.time.delay(3)

            self.music_manager.activate_effect('punch')

            while self.position[0] >= self.ends[2]:
                self.position[0] -= self.steps[2]
                pygame.time.delay(3)

            while self.position[0] >= self.ends[3]:
                self.position[0] -= self.steps[3]
                pygame.time.delay(3)

        elif self.side == 'right':
            while self.position[0] >= self.ends[0]:
                self.position[0] += self.steps[0]
                pygame.time.delay(3)

            while self.position[0] >= self.ends[1]:
                self.position[0] += self.steps[1]
                pygame.time.delay(3)

            self.music_manager.activate_effect('punch')

            while self.position[0] <= self.ends[2]:
                self.position[0] -= self.steps[2]
                pygame.time.delay(3)

            while self.position[0] <= self.ends[3]:
                self.position[0] -= self.steps[3]
                pygame.time.delay(3)

    def attack(self) -> int:
        '''Метод получения урона от атаки'''
        return 10 * self.characteristics['str'] * self.characteristics['dex'] + randint(1, 5) - randint(1, 5)

    def magic(self) -> int:
        '''Метод получения урона от магии'''
        self.characteristics['mp'] -= self.characteristics['int'] * 2 + 2
        return 15 * self.characteristics['int'] + randint(1, 10) - randint(1, 10)

    def get_damage(self, damage: int) -> None:
        '''Метод получения урона'''
        if damage < 0:
            damage = 0
        self.characteristics['hp'] -= damage

    def set_damage(self, move: str) -> int:
        '''Метод нанесения урона'''
        if move == 'attack':
            return self.attack()
        elif move == 'magic':
            if not self.characteristics['mp'] <= 0:
                return self.magic()
        return 0

    @order_for_queue
    def magic_animation(self) -> None:
        '''Метод анимации магии'''
        if self.side == 'left':
            position = 150
            self.screen: pygame.Surface
            while position <= self.ends[4]:
                self.screen.blit(self.fireball, (position, 540))
                position += self.steps[4]
                pygame.time.delay(5)
            self.music_manager.activate_effect('boom')
        elif self.side == 'right':
            position = 1920 - 150 - self.texture.get_width()
            self.screen: pygame.Surface
            while position >= self.ends[4]:
                self.screen.blit(self.fireball, (position, 540))
                position += self.steps[4]
                pygame.time.delay(5)
            self.music_manager.activate_effect('boom')

    def get_hp_percent(self) -> float:
        '''Метод получения количества жизни в процентах'''
        return self.characteristics['hp'] * 100 / self.get_max_hp() / 100

    def get_mp_percent(self) -> float:
        '''Метод получения маны в процентах'''
        return self.characteristics['mp'] * 100 / self.get_max_mp() / 100

    def get_max_hp(self) -> float:
        '''Метод получения предельной жизни'''
        return self.characteristics['max_hp']

    def get_max_mp(self) -> float:
        '''Метод получения предельной маны'''
        return self.characteristics['max_mp']


class BattleQueue:
    '''Метод очереди битвы'''
    def __init__(self) -> None:
        self.present_attendee = False  # False - player, True - enemy

    def is_player_queue(self) -> bool:
        '''Метод получения очереди игрока'''
        if self.present_attendee:
            return False
        return True

    def is_enemy_queue(self) -> bool:
        '''Метод получения очереди противника'''
        if self.present_attendee:
            return True
        return False

    def change_queue(self) -> None:
        '''Метод передачи очереди'''
        self.present_attendee = not self.present_attendee

    def get_present_queue(self) -> bool:
        '''Метод получения очереди'''
        return self.present_attendee

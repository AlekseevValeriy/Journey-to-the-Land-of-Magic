import pygame

from button import ButtonObject


class StatusBar(ButtonObject):
    '''Класс панели персонажа'''

    def __init__(self, screen: pygame.Surface, *buttons, **data) -> None:
        super().__init__(screen, *buttons, **data)
        self.add_data(exp=0, hp=0, mp=0, level=0,
                      min_exp=10, min_hp=100, min_mp=20,
                      exp_multiplier=1.3, hp_multiplier=1.4, mp_multiplier=1.2,
                      max_level=20, persona_status=False)
        self.born()

    def update_lines(self) -> None:
        '''Метод обновления полосок параметров'''
        exp_percent = (self.data['exp'] * 100) // self.max_characteristic('exp') / 100
        hp_percent = (self.data['hp'] * 100) // self.max_characteristic('hp') / 100
        mp_percent = (self.data['mp'] * 100) // self.max_characteristic('mp') / 100
        self.buttons[6].size[0] = self.buttons[6].texture[self.buttons[6].status].get_width() * exp_percent
        self.buttons[7].size[0] = self.buttons[7].texture[self.buttons[7].status].get_width() * hp_percent
        self.buttons[8].size[0] = self.buttons[8].texture[self.buttons[8].status].get_width() * mp_percent
        self.change_dead_frame_alpha(hp_percent)

    def add_parameter(self, parameter, number) -> None:
        '''Метод увелечения параметра'''
        if parameter in ['exp', 'hp', 'mp']:
            self.data[parameter] += number
            max_char = self.max_characteristic(parameter)
            if self.data[parameter] > max_char:
                self.data[parameter] = max_char

    def reduce_parameter(self, parameter: str, number: int) -> None:
        '''Метод уменьшения параметра'''
        if parameter in ['exp', 'hp', 'mp']:
            self.data[parameter] -= number
            if self.data[parameter] < 0:
                self.data[parameter] = 0

    def get_chips(self) -> tuple:
        '''Метод получения осколка'''
        return self.data['chip_1'], self.data['chip_2'], self.data['chip_3'], self.data['chip_4']

    def change_dead_frame_alpha(self, hp_percent: float) -> None:
        '''Метод изменения окраски окна персонажа'''
        if hp_percent <= 0.5:
            if hp_percent > 0:
                alpha = (4 * 0.5 // hp_percent * 8)
            else:
                alpha = (4 * 0.5 // 0.1 * 8)
            self.buttons[9].texture[self.buttons[9].status].set_alpha(alpha)

    def max_characteristic(self, characteristic: str, **characteristic_data) -> int:
        '''Метод получения максимальной характеристики'''
        if characteristic in ['exp', 'hp', 'mp']:
            return self.data[f'min_{characteristic}'] * (
                    self.data[f'{characteristic}_multiplier'] ** self.data['level'])
        elif characteristic == 'm_exp':
            return characteristic_data['m_exp'] * (
                    characteristic_data[f'{characteristic}_multiplier'] ** self.data['level'])
        return 0

    def born(self) -> None:
        '''Метод обновления параметров'''
        self.data['persona_status'] = True
        self.buttons[9].texture[self.buttons[9].status].set_alpha(0)
        self.data['hp'] = self.max_characteristic('hp')
        self.data['mp'] = self.max_characteristic('mp')

    def level_up_check(self) -> None:
        '''Метод проверки поднятия уровня'''
        if self.data['exp'] >= self.max_characteristic('exp'):
            self.level_up()

    def level_up(self) -> None:
        '''Метод поднятия уровня'''
        self.data['level'] += 1
        self.data['exp'] = 0
        self.data['hp'] = self.max_characteristic('hp')
        self.data['mp'] = self.max_characteristic('mp')
        self.data['free_points'] += 2
        self.data['magic_free_points'] += 1

    def dead_check(self) -> None:
        '''Метод проверки на смерть'''
        if self.data['hp'] <= 0:
            self.dead()

    def dead(self) -> None:
        '''Метод смерти персонажа'''
        self.data['persona_status'] = False
        self.data['hp'] = 0
        self.data['mp'] = 0
        self.data['exp'] -= self.max_characteristic('m_exp', m_exp=5, m_exp_multiplier=1.2)
        if self.data['exp'] < 0:
            self.data['exp'] = 0

    def get_persona_status(self) -> bool:
        '''Метод поучения статуса персонажа'''
        return self.data['persona_status']

    def get_player_data(self) -> dict:
        '''Метод получения данных персонажа'''
        return self.data

    def get_characteristics(self) -> dict:
        '''Метод получения характеристик персонажа'''
        return {'str_points': self.data['str'], 'dex_points': self.data['dex'], 'int_points': self.data['int'],
                "free_points": self.data['free_points']}

    def get_magic_data(self) -> dict:
        '''Метод получения характеристик магии персонажа'''
        return {'free_points': self.data['magic_free_points'], 'fb_get': self.data['fb_get'],
                'fb_level': self.data['fb_level']}

    def draw(self) -> None:
        '''Метод отрисовки панели'''
        self.update_lines()
        for button in self.buttons:
            button.draw()

    def get_points(self) -> tuple:
        '''Метод получения очков улучшения'''
        return self.data['magic_free_points'], self.data['free_points']

    def clear_points(self) -> None:
        '''Метод очистки очков улучшения'''
        self.data['magic_free_points'] = 0
        self.data['free_points'] = 0


class WorldMap(ButtonObject):
    '''Класс мини-карты'''

    def __init__(self, screen: pygame.Surface, *buttons, **data):
        super().__init__(screen, *buttons, **data)
        self.add_data(player_position=(0, 0), world_map=[[]], frame=(0, 0), map_sector=100,
                      map_surface=pygame.Surface((260, 260)),
                      colors={0: 'black', False: 'black', 1: (51, 51, 51), 2: (102, 102, 102), 3: (128, 128, 128),
                              4: (153, 153, 153), 5: (179, 179, 179), 6: (204, 204, 204), 12: (220, 220, 220),
                              13: (135, 135, 135), 10: (110, 110, 110), 20: (230, 230, 230)}, sector_size=10,
                      map_start=(1615, 45),
                      frame_size=140,
                      render_frame_x=(-14, 12), render_frame_y=(-14, 12), camera_position=(0, 0), black=False,
                      other_positions=(), world_size=None)

    def set_world_map(self, world_map: list) -> None:
        '''Метод установки карты'''
        self.data['world_map'] = world_map
        self.data['world_size'] = (len(world_map[0][0]), len(world_map[0]))

    def set_other_positions(self, other_positions: tuple) -> None:
        '''Метод установки позиции'''
        self.data['other_positions'] = other_positions

    def set_player_position(self, player_position: tuple) -> None:
        '''Метод установки позиции игрока'''
        self.data['player_position'] = player_position

    def set_frame(self, frame: tuple) -> None:
        '''Метод установки рамки'''
        self.data['frame'] = frame

    def get_player_position(self) -> dict:
        '''Метод получения позиции'''
        return {"player_position": self.data['player_position']}

    def draw(self) -> None:
        '''Метод отрисовки карты'''
        if self.data['black']:
            self.data['map_surface'].fill('black')
        frame_size = self.data['frame_size']
        se_si = self.data['sector_size']
        for button in self.buttons:
            button.draw()
        x_index = (self.data['player_position'][0] + self.data['frame'][0] + 960) // self.data['map_sector']
        y_index = (self.data['player_position'][1] + self.data['frame'][1] + 540) // self.data['map_sector']
        for z in range(len(self.data['world_map'])):
            for y in range(*self.data['render_frame_y']):
                for x in range(*self.data['render_frame_x']):
                    if 0 <= (x_index + x) < self.data['world_size'][0] and 0 <= (y_index + y) < self.data['world_size'][
                        1]:
                        if self.data['world_map'][z][y_index + y][x_index + x] != -1:
                            color = self.data['colors'][int(self.data['world_map'][z][y_index + y][x_index + x])]
                            if color:
                                pygame.draw.rect(surface=self.data['map_surface'], color=color,
                                                 rect=(frame_size + se_si * x + self.data['camera_position'][0],
                                                       frame_size + se_si * y + self.data['camera_position'][1], se_si,
                                                       se_si))
                    else:
                        pygame.draw.rect(surface=self.data['map_surface'], color='black',
                                         rect=(frame_size + se_si * x + self.data['camera_position'][0],
                                               frame_size + se_si * y + self.data['camera_position'][1], se_si, se_si))

        pygame.draw.rect(surface=self.data['map_surface'], color=(128, 128, 128),
                         rect=(
                             frame_size + self.data['camera_position'][0], frame_size + self.data['camera_position'][1],
                             se_si,
                             se_si))
        # TODO улучшить точность карты и добавить врагов на мини-карту
        if self.data['other_positions']:
            for x, y in self.data['other_positions']:
                pygame.draw.rect(surface=self.data['map_surface'], color=(128, 128, 128),
                                 rect=(frame_size + se_si * (
                                         (x - self.data['player_position'][0]) // self.data['map_sector']) +
                                       self.data['camera_position'][0], frame_size + se_si * (
                                               (y - self.data['player_position'][1]) // self.data['map_sector']) +
                                       self.data['camera_position'][1], se_si, se_si))

        self.screen.blit(self.data['map_surface'], self.data['map_start'])


class SkillUpgrade(ButtonObject):
    '''Класс элементов улучшения персонажа'''

    def __init__(self, screen: pygame.Surface, *buttons, **data) -> None:
        super().__init__(screen, *buttons, **data)
        self.add_data(free_points=0, str_points=0, dex_points=0, int_points=0)

    def is_upgradeable(self) -> bool:
        '''Метод проверки на улучшение'''
        if self.data['free_points']:
            return True
        return False

    def add_point(self, characteristic: str) -> None:
        '''Метод добавления очков'''
        if self.data['free_points']:
            self.data[f'{characteristic}_points'] += 1
            self.data['free_points'] -= 1
        self.update_points()

    def get_characteristics(self) -> tuple:
        '''Метод получения характеристик'''
        return self.data['str_points'], self.data['dex_points'], self.data['int_points'], self.data['free_points']

    def update_points(self) -> None:
        '''Метод обновления очков'''
        self.buttons[0].text = str(self.data['str_points'])
        self.buttons[1].text = str(self.data['dex_points'])
        self.buttons[2].text = str(self.data['int_points'])
        self.buttons[3].text = str(self.data['free_points'])


class MagicUpgrade(ButtonObject):
    '''Класс элементов магического улучшения персонажа'''

    def __init__(self, screen: pygame.Surface, *buttons, **data) -> None:
        super().__init__(screen, *buttons, **data)
        self.add_data(free_points=0, fb_get=False, fb_level=0)

    def add_point(self) -> None:
        '''Метод добавления очка'''
        if self.data['free_points']:
            if not self.data['fb_get']:
                self.data['fb_get'] = True
            self.data['fb_level'] += 1
            self.data['free_points'] -= 1
        self.update_points()

    def have_fb(self) -> bool:
        '''Метод проверки на наличие магии'''
        if self.data['fb_get']:
            return True
        return False

    def get_characteristics(self) -> tuple:
        '''Метод получения характеристик'''
        return self.data['fb_get'], self.data['fb_level'], self.data['free_points']

    def is_upgradeable(self) -> bool:
        '''Метод проверки на улучшение'''
        if self.data['free_points']:
            return True
        return False

    def update_points(self) -> None:
        '''Метод обновления очков'''
        self.buttons[0].text = str(self.data['fb_level'])
        self.buttons[1].text = str(self.data['free_points'])


class BigMap(WorldMap):
    '''Класс большой карты'''

    def __init__(self, screen: pygame.Surface, *buttons, **data) -> None:
        super().__init__(screen, *buttons, **data)
        self.add_data(start_sector_size=10, sector_size=10, camera_position=(0, 0), sector_size_multiplier=1,
                      map_start=(500, 90), frame_size=400, map_surface=pygame.Surface((900, 900)),
                      black=True)
        self.change_render_frame()

    def change_sector_size(self, symbol: int) -> None:
        '''Метод смены размера элемента карты'''
        self.data['sector_size_multiplier'] += symbol
        if self.data['sector_size_multiplier'] < 0.2:
            self.data['sector_size_multiplier'] = 0.2
        elif self.data['sector_size_multiplier'] > 10:
            self.data['sector_size_multiplier'] = 10
        self.data['sector_size'] = self.data['start_sector_size'] * self.data['sector_size_multiplier']
        self.change_render_frame()

    def change_render_frame(self) -> None:
        '''Метод смены окна карты'''
        nfxs = int((self.data['map_surface'].get_width() // self.data['sector_size']) // 2) + 2 + int(
            self.data['camera_position'][0] // self.data['sector_size'])
        nfxe = int((self.data['map_surface'].get_width() // self.data['sector_size']) // 2) + 2 - int(
            self.data['camera_position'][0] // self.data['sector_size'])
        self.data['render_frame_x'] = (-nfxs, nfxe + 10)
        nfys = int((self.data['map_surface'].get_height() // self.data['sector_size']) // 2) + 2 + int(
            self.data['camera_position'][1] // self.data['sector_size'])
        nfye = int((self.data['map_surface'].get_height() // self.data['sector_size']) // 2) + 2 - int(
            self.data['camera_position'][1] // self.data['sector_size'])
        self.data['render_frame_y'] = (-nfys, nfye + 10)

    def in_map(self, mouse_position) -> bool:
        '''Метод проверки курсора в карте'''
        if ((self.data['map_start'][0] < mouse_position[0] < (
                self.data['map_start'][0] + self.data['map_surface'].get_width())) and
                (self.data['map_start'][1] < mouse_position[1] < (
                        self.data['map_start'][1] + self.data['map_surface'].get_height()))):
            return True
        return False

    def position_move(self, position: tuple) -> None:
        '''Метод установки позиции'''
        self.data['camera_position'] = (self.data['camera_position'][0] + position[0],
                                        self.data['camera_position'][1] + position[1])
        self.change_render_frame()

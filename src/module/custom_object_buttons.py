import pygame

from button import ButtonObject


class StatusBar(ButtonObject):
    def __init__(self, screen, *buttons, **data):
        super().__init__(screen, *buttons, **data)
        self.add_data(exp=0, hp=0, mp=0, level=0,
                      min_exp=10, min_hp=100, min_mp=20,
                      exp_multiplier=1.3, hp_multiplier=1.4, mp_multiplier=1.2,
                      max_level=20, persona_status=False)
        self.born()

    def update_lines(self):
        exp_percent = (self.data['exp'] * 100) // self.max_characteristic('exp') / 100
        hp_percent = (self.data['hp'] * 100) // self.max_characteristic('hp') / 100
        mp_percent = (self.data['mp'] * 100) // self.max_characteristic('mp') / 100
        self.buttons[6].size[0] = self.buttons[6].texture[self.buttons[6].status].get_width() * exp_percent
        self.buttons[7].size[0] = self.buttons[7].texture[self.buttons[7].status].get_width() * hp_percent
        self.buttons[8].size[0] = self.buttons[8].texture[self.buttons[8].status].get_width() * mp_percent
        self.change_dead_frame_alpha(hp_percent)

    def add_parameter(self, parameter, number):
        if parameter in ['exp', 'hp', 'mp']:
            self.data[parameter] += number
            max_char = self.max_characteristic(parameter)
            if self.data[parameter] > max_char:
                self.data[parameter] = max_char

    def reduce_parameter(self, parameter, number):
        if parameter in ['exp', 'hp', 'mp']:
            self.data[parameter] -= number
            if self.data[parameter] < 0:
                self.data[parameter] = 0

    def change_dead_frame_alpha(self, hp_percent):
        if hp_percent <= 0.5:
            if hp_percent > 0:
                alpha = (4 * 0.5 // hp_percent * 8)
                self.buttons[9].texture[self.buttons[9].status].set_alpha(alpha)

    def max_characteristic(self, characteristic: str, **characteristic_data) -> int:
        if characteristic in ['exp', 'hp', 'mp']:
            return self.data[f'min_{characteristic}'] * (
                    self.data[f'{characteristic}_multiplier'] ** self.data['level'])
        elif characteristic == 'm_exp':
            return characteristic_data['m_exp'] * (
                    characteristic_data[f'{characteristic}_multiplier'] ** self.data['level'])
        return 0

    def born(self):
        self.data['persona_status'] = True
        self.buttons[9].texture[self.buttons[9].status].set_alpha(0)
        self.data['hp'] = self.max_characteristic('hp')
        self.data['mp'] = self.max_characteristic('mp')

    def level_up_check(self):
        if self.data['exp'] >= self.max_characteristic('exp'):
            self.level_up()

    def level_up(self):
        self.data['level'] += 1
        self.data['exp'] = 0
        self.data['hp'] = self.max_characteristic('hp')
        self.data['mp'] = self.max_characteristic('mp')

    def dead_check(self):
        if self.data['hp'] <= 0:
            self.dead()

    def dead(self):
        self.data['persona_status'] = False
        self.data['hp'] = 0
        self.data['mp'] = 0
        self.data['exp'] -= self.max_characteristic('m_exp', m_exp=5, m_exp_multiplier=1.2)
        if self.data['exp'] < 0:
            self.data['exp'] = 0

    def get_persona_status(self) -> bool:
        return self.data['persona_status']

    def draw(self):
        self.update_lines()
        for button in self.buttons:
            button.draw()


class WorldMap(ButtonObject):
    def __init__(self, screen, *buttons, **data):
        super().__init__(screen, *buttons, **data)
        self.add_data(player_position=(0, 0), world_map=[[]], map_sector=100, map_surface=pygame.Surface((260, 260)),
                      colors={0: False, 1: 'green', 2: 'orange'})

    def set_world_map(self, world_map):
        self.data['world_map'] = world_map

    def set_player_position(self, player_position):
        self.data['player_position'] = player_position

    def draw(self):
        for button in self.buttons:
            button.draw()

            # TODO дальше сделать остальные кнопки для перехода по меню игры
        x_index = (self.data['player_position'][0] + 960) // self.data['map_sector']
        y_index = (self.data['player_position'][1] + 540) // self.data['map_sector']
        for z in range(len(self.data['world_map'])):
            for y in range(-14, 12):
                for x in range(-14, 12):
                    if 0 <= (x_index + x) < len(self.data['world_map'][0]) and 0 <= y_index + y < len(
                            self.data['world_map'][0][0]):
                        color = self.data['colors'][int(self.data['world_map'][z][y_index + y][x_index + x])]
                        if color:
                            pygame.draw.rect(surface=self.data['map_surface'], color=color,
                                             rect=(140 + 10 * x, 140 + 10 * y, 10, 10))
                    else:
                        pygame.draw.rect(surface=self.data['map_surface'], color='blue',
                                         rect=(140 + 10 * x, 140 + 10 * y, 10, 10))
        pygame.draw.rect(surface=self.data['map_surface'], color='red',
                         rect=(140, 140, 10, 10))
        self.screen.blit(self.data['map_surface'], (1615, 45))


if __name__ == '__main__':
    b = StatusBar('screen', 'b1', 'b2', 'b3', hp=10, mp=20, exp=30)

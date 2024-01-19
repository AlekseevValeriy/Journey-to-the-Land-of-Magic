from os import listdir

from pygame import Surface
from pygame.image import load
from music_manager import MusicManager
from json_reader import JsonReader


class Player:
    '''Класс персонажа'''
    def __init__(self, screen: Surface, position: tuple, person: str, **personal_data) -> None:
        self.music_manager = MusicManager(0.5)
        value = (JsonReader.read_file('../../data/json/settings_data.json')['volume_trigger_position'] - 816) * 100 // (
                1100 - 816) / 100
        if value > 1:
            value = 1
        if value < 0:
            value = 0
        self.music_manager.set_volume(value)
        self.personal_data = personal_data
        self.screen = screen
        self.position: list = list(position)
        self.person = person
        self.step_on_30_frame_rate = 12 * 1
        self.frame_skip_quality_on_30_frame_rate = 2
        self.frame_skip_quality = self.frame_skip_quality_on_30_frame_rate
        self.frame_skip = 0
        self.present_step = self.step_on_30_frame_rate
        self.face_side = 'down'  # can be: down, up, left, right
        self.move_status = 'stand'  # can be: stand, run
        self.present_texture = 'down_run_0'
        self.textures = {}
        self.size = ()
        if self.person:
            for image in listdir(f"../../data/textures/player/{self.person}"):
                self.textures[image.removesuffix('.png')] = load('/'.join([f"../../data/textures/player/{self.person}",
                                                                           image])).convert_alpha()
        FRAME = 150
        self.run_frame_size = [FRAME, FRAME]
        self.run_frame_move = [0, 0]
        self.last_move = [0, 0]
        self.fake_pos = None


    def get_personal_data(self) -> dict:
        '''Метод получения данных'''
        return self.personal_data

    def change_position(self, sign: int, axis: int, where=None) -> None:
        '''Метод смены позиции персонажа'''
        if where:
            self.fake_pos = list(self.get_position_sp())
            self.fake_pos[axis] = self.position[axis] + self.frame_inspector(axis, self.present_step * sign)
        else:
            self.position[axis] = self.position[axis] + self.frame_inspector(axis, self.present_step * sign)
            self.set_last_move(axis=axis, step=self.position[axis] + self.present_step * sign)

    def sample_change_position(self, sign: int, axis: int) -> None:
        '''Метод смены положения'''
        self.position[axis] = self.position[axis] + self.present_step * sign


    def change_animation_under_fps(self, frame_rate: int) -> None:
        '''Метод настройки данных под данный fps'''
        self.present_step = (self.step_on_30_frame_rate * 30) // frame_rate
        self.frame_skip_quality = (self.frame_skip_quality_on_30_frame_rate * frame_rate) // 30

    def get_frame(self) -> list:
        '''Метод для получения кадра неподвижной камеры'''
        return self.run_frame_move

    def get_position(self) -> list:
        '''Метод получения позиции персонажа'''
        return self.position

    def get_position_fr(self) -> tuple:
        '''Метод получения позиции персонажа с рамкой'''
        return self.position[0] + self.run_frame_move[0], self.position[1] + self.run_frame_move[1]

    def get_position_sp(self) -> tuple:
        '''Метод получения позиции с рамкой с экраном'''
        return self.position[0] + 960 + self.run_frame_move[0], self.position[1] + 540 + self.run_frame_move[1]

    @staticmethod
    def position_as_sp(position: tuple) -> tuple:
        '''Метод для конвертации данной позиции в специальную'''
        return position[0] + 960, position[1] + 540

    def get_fr_pos(self) -> tuple:
        '''Метод получения позиции'''
        return tuple(i - j for i, j in zip(self.get_position(), self.get_frame()))

    def set_face_side(self, face_side: str) -> None:
        '''Метод для смены направления персонажа'''
        self.face_side = face_side

    def set_size(self, size: tuple) -> None:
        '''Метод для постановки размера'''
        self.size = size

    def get_p_size(self) -> tuple:
        '''Метод для получения размера'''
        return self.size

    def texture_selection(self) -> None:
        '''Метод для смены текстуры'''
        if self.frame_skip != self.frame_skip_quality:
            self.frame_skip = (self.frame_skip + 1) % (self.frame_skip_quality + 1)
        else:
            self.frame_skip = 0
            if self.move_status == 'stand':
                self.present_texture = f"{self.face_side}_run_0"
            elif self.move_status == 'run':
                self.present_texture = f"{self.face_side}_run_{(int(self.present_texture.split('_')[-1]) + 1) % 4}"

    def draw_player(self) -> None:
        '''Метод для отрисовки игрока'''
        self.texture_selection()
        texture = self.textures.get(self.present_texture, self.textures['up_run_0'])
        self.screen.blit(texture, [(self.screen.get_width() // 2 + self.run_frame_move[0]) - texture.get_width() // 2,
                                   (self.screen.get_height() // 2 + self.run_frame_move[
                                       1]) - texture.get_height() // 2])

    def clear_frame_skip(self) -> None:
        '''Метод для очистки счётчика пропуска кадров'''
        self.frame_skip = 0

    def frame_inspector(self, axis: int, step: int) -> int:
        '''Метод проверки кадра'''
        if ((step < 0 and self.run_frame_move[axis] > -self.run_frame_size[axis]) or
                (step > 0 and self.run_frame_move[axis] < self.run_frame_size[axis])):
            self.run_frame_move[axis] += step
            return 0
        return step

    def player_move(self, status: str, where=None) -> None:
        '''Метод движения персонажа'''
        self.move_status = status
        if self.move_status == 'run':
            if int(self.present_texture.split('_')[-1]) in (1, 3):
                self.music_manager.activate_effect('run')
            if self.face_side == 'up':
                if where:
                    self.change_position(-1, 1, where)
                else:
                    self.change_position(-1, 1)
            elif self.face_side == 'down':
                if where:
                    self.change_position(1, 1, where)
                else:
                    self.change_position(1, 1)
            elif self.face_side == 'left':
                if where:
                    self.change_position(-1, 0, where)
                else:
                    self.change_position(-1, 0)
            elif self.face_side == 'right':
                if where:
                    self.change_position(1, 0, where)
                else:
                    self.change_position(1, 0)

    def sample_move(self, status: str) -> None:
        '''Метод движения для врагов'''
        self.move_status = status
        if self.move_status == 'run':
            if self.face_side == 'up':
                self.sample_change_position(-1, 1)
            elif self.face_side == 'down':
                self.sample_change_position(1, 1)
            elif self.face_side == 'left':
                self.sample_change_position(-1, 0)
            elif self.face_side == 'right':
                self.sample_change_position(1, 0)

    def set_last_move(self, move=None, axis=None, step=None) -> None:
        '''Метод установки последнего движения'''
        if move:
            self.last_move = move
        else:
            if axis:
                self.last_move = (0, step)
            else:
                self.last_move = (step, 0)

    def replace_last_move(self) -> None:
        '''Метод смен последнего движения'''
        self.position = [self.position[0] - self.last_move[0], self.position[1] - self.last_move[1]]

    def fake_move(self) -> tuple:
        '''Метод для получения положения перед движением'''
        self.player_move('run', True)
        return self.fake_pos

    def __str__(self):
        return self.position

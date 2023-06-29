import pygame


class MusicStation:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        # self.music_game = pygame.mixer.Sound('Game_柊キライ fea. flower - エバ.mp3')
        self.process_flag = True
        self.sound = {}

    def add_sound(self, specialization, sound_name, path_of_sound, status='not_running'):
        self.sound[specialization] = {}
        self.sound[specialization][sound_name] = [pygame.mixer.Sound(path_of_sound), status]

    def delete_sound(self, specialization, sound_name):
        if self.sound[specialization][sound_name][1] == 'not_running':
            self.sound[specialization].pop(sound_name, False)
        else:
            self.sound[specialization][sound_name].pause()
            self.sound[specialization].pop(sound_name, False)

    def start_sound(self, specialization, sound_name):
        if self.sound[specialization][sound_name][1] == 'not_running':
            self.sound[specialization][sound_name][0] = self.sound[specialization][sound_name][0].play(-1)
            self.sound[specialization][sound_name][1] = 'running'
        elif self.sound[specialization][sound_name][1] == 'running':
            self.sound[specialization][sound_name][0].unpause()

    def pause(self, specialization, sound_name):
        if self.process_flag:
            self.sound[specialization][sound_name][0].pause()

    def unpause(self, specialization, sound_name):
        if self.process_flag:
            self.sound[specialization][sound_name][0].unpause()


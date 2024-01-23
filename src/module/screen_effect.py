from time import sleep

import pygame


class ScreenEffect:
    '''Класс для специальных движений'''

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, frame_rate: int) -> None:
        self.screen = screen
        self.clock = clock
        self.frame_rate = frame_rate

    def game_intro(self) -> None:
        '''Метод визуализации интро игры'''
        logo = EffectElement(self.screen, pygame.image.load("../../data/textures/Game_Logo.png").convert_alpha(),
                             (960, 540), -70)
        text = pygame.font.Font('..//..//data//fonts//Book Antiqua.ttf', 18).render(
            'Команда VaTi представляет', True,'white')
        text = EffectElement(self.screen, text,
                             (960, 650), 0)
        effects_flags = [False, False]
        alpha_step = 3.75
        animation = True
        sleep(1.5)
        while animation:
            if not effects_flags[0] and logo.get_alpha() < 255:
                logo.add_alpha(alpha_step)
            elif not effects_flags[0] and logo.get_alpha() == 255:
                effects_flags[0] = True
            if not effects_flags[1] and effects_flags[0] and text.get_alpha() < 255:
                text.add_alpha(alpha_step)
            elif not effects_flags[1] and effects_flags[0] and text.get_alpha() == 255:
                effects_flags[1] = True
            if effects_flags[0] and effects_flags[1]:
                logo.add_alpha(-alpha_step)
                text.add_alpha(-alpha_step)
            if logo.get_alpha() == 0 and text.get_alpha() == 0 and effects_flags[0] and effects_flags[1]:
                animation = False
            self.screen.fill((0, 0, 0))
            logo.draw()
            text.draw()
            pygame.display.update()
            self.clock.tick(self.frame_rate)

    def battle_end_animation(self, exodus: str) -> None:
        '''Метод для визуализации интро окончания битвы'''
        font = pygame.font.Font('..//..//data//fonts//better-vcr-5.2(for eng).ttf', 100)
        text = font.render(exodus, True, 'white')
        text.set_alpha(6)

        pelena = pygame.Surface((1920, 1080))
        pelena.set_alpha(6)
        pelena.fill((0, 0, 0))

        counter = 0

        while counter <= 129:
            counter += 1
            self.screen.blit(pelena, (0, 0))
            pygame.display.update()
            self.clock.tick(self.frame_rate)

        counter = 0
        dest = (1920 // 2 - text.get_width() // 2, 1080 // 2 - text.get_height() // 2)
        while counter <= 129:
            counter += 1
            self.screen.blit(text, dest)
            pygame.display.update()
            self.clock.tick(self.frame_rate)


class EffectElement:
    '''Класс элементов визуализации'''

    def __init__(self, screen: pygame.Surface, surface: pygame.time.Clock, position: tuple, alpha: int):
        self.screen = screen
        self.surface = surface
        self.alpha = alpha
        self.surface.set_alpha(self.alpha)
        self.position = list(position)
        self.position[0] -= self.surface.get_width() / 2
        self.position[1] -= self.surface.get_height() / 2

    def draw(self):
        '''Метод отрисовки эффекта'''
        self.surface.set_alpha(self.alpha)
        self.screen.blit(source=self.surface, dest=(self.position, self.surface.get_size()))

    def add_alpha(self, alpha):
        '''Метод установки альфа канала'''
        if 0 <= self.surface.get_alpha() <= 255:
            self.alpha = self.surface.get_alpha() + alpha

    def get_alpha(self):
        '''Метод получения альфа канала'''
        return self.surface.get_alpha()

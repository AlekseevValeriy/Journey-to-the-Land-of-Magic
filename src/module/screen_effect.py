import pygame
from time import sleep


class ScreenEffect:
    def __init__(self, screen, clock, frame_rate):
        self.screen: pygame.Surface = screen
        self.clock = clock
        self.frame_rate = frame_rate

    def game_intro(self):
        logo = EffectElement(self.screen, pygame.image.load("../../data/textures/Game_Logo.png").convert_alpha(),
                             (960, 540), -70)
        text = pygame.font.Font('..//..//data//fonts//Book Antiqua.ttf', 18).render('Команда VaTi представляет', True,
                                                                                    'white')
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

    def battle_end_animation(self, exodus):
        font = pygame.font.Font('..//..//data//fonts//better-vcr-5.2(for eng).ttf', 100)
        text = font.render(exodus, 'white')
        black_surface = pygame.Surface((1920, 1080))
        pygame.draw.rect(surface=black_surface, color=(0, 0, 0, 250), rect=(0, 0, 1920, 1080))
        counter = 0
        while counter <= 129:
            self.screen.blit(black_surface)
            sleep(0.1)
            pygame.display.update()
            self.clock.tick(self.frame_rate)


class EffectElement:
    def __init__(self, screen, surface, position, alpha):
        self.screen = screen
        self.surface: pygame.Surface = surface
        self.alpha = alpha
        self.surface.set_alpha(self.alpha)
        self.position = list(position)
        self.position[0] -= self.surface.get_width() / 2
        self.position[1] -= self.surface.get_height() / 2

    def draw(self):
        self.surface.set_alpha(self.alpha)
        self.screen.blit(source=self.surface, dest=(self.position, self.surface.get_size()))

    def add_alpha(self, alpha):
        if 0 <= self.surface.get_alpha() <= 255:
            self.alpha = self.surface.get_alpha() + alpha

    def get_alpha(self):
        return self.surface.get_alpha()

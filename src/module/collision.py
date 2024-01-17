import pygame

blocked_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

class Collision:
    def __init__(self):
        self.player_sprite = None

    def set_player_sprite(self, position: tuple, sprite_size: tuple):
        self.player_sprite = Player(position, sprite_size)

    def set_player_position(self, position):
        if self.player_sprite:
            self.player_sprite.rect.x, self.player_sprite.rect.y = position

    def clear(self):
        self.player_sprite = None
        player_group = pygame.sprite.Group
        blocked_group = pygame.sprite.Group

    def add_block(self, position, sprite_size):
        Block(position, sprite_size)

    def co_co_in(self, player_position): # collision_conflict_inspector
        self.set_player_position(player_position)
        return pygame.sprite.spritecollideany(self.player_sprite, blocked_group)

class Player(pygame.sprite.Sprite):
    def __init__(self, position, sprite_size):
        super().__init__(player_group)
        self.rect = pygame.Rect(*position, *sprite_size)

class Block(pygame.sprite.Sprite):
    def __init__(self, position, sprite_size):
        super().__init__(blocked_group)
        self.rect = pygame.Rect(*position, *sprite_size)
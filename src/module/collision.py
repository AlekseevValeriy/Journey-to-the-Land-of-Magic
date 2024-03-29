import pygame

blocked_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Collision:
    '''Класс коллизии объектов'''

    def __init__(self) -> None:
        self.player_sprite = None

    def set_player_sprite(self, position: tuple, sprite_size: tuple) -> None:
        '''Метод создания спрайта персонажа'''
        self.player_sprite = Player(position, sprite_size)

    def set_player_position(self, position: tuple) -> None:
        '''Метод установки позиции персонажа'''
        if self.player_sprite:
            self.player_sprite.rect.x, self.player_sprite.rect.y = position

    def clear(self) -> None:
        '''Метод очистки коллизий'''
        self.player_sprite = None
        player_group.empty()
        blocked_group.empty()

    def clear_blocks(self) -> None:
        '''Метод очистки блоков'''
        blocked_group.empty()

    def add_block(self, position: tuple, sprite_size: tuple) -> None:
        '''Метод добавления блоков'''
        Block(position, sprite_size)

    def co_co_in(self, player_position: tuple):  # collision_conflict_inspector
        '''Метод коллизии'''
        self.set_player_position(player_position)
        return pygame.sprite.spritecollideany(self.player_sprite, blocked_group)


class Player(pygame.sprite.Sprite):
    '''Класс спрайта персонажа'''

    def __init__(self, position: tuple, sprite_size: tuple) -> None:
        super().__init__(player_group)
        self.rect = pygame.Rect(*position, *sprite_size)


class Block(pygame.sprite.Sprite):
    '''Класс спрайта блока'''

    def __init__(self, position: tuple, sprite_size: tuple) -> None:
        super().__init__(blocked_group)
        self.rect = pygame.Rect(*position, *sprite_size)

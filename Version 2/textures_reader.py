from os import listdir, path
from pygame.image import load


class TexturesReader:
    def __init__(self, path):
        self.path = path
        self.textures = listdir(path)

    def get_textures(self, sort_type):
        self.chose_sort(sort_type)
        for directory in self.textures:
            for texture in enumerate(self.textures[directory]):
                self.textures[directory][texture[0]] = load(path.join(self.path, texture[1])).convert_alpha()
        return self.textures

    def player_sort(self):
        sorted_textures = {'up': [], 'down': [], 'left': [], 'right': []}
        for texture in self.textures:
            sorted_textures[texture.split('_')[0]].append(texture)
        self.textures = sorted_textures

    def chose_sort(self, sort_type):
        if sort_type == 'player':
            self.player_sort()

import pygame
import os

class SpriteSheet:
    def __init__(self, image, directory=None):
        self.image_name = image
        self.image = pygame.image.load(os.path.join(directory, self.image_name) if directory else os.path.join(self.image_name))
        self.image_size = self.image.get_size()
        self.folder = os.getcwd()
        self.file_list = os.listdir(os.getcwd())
        self.counter = 0

    def make_directory(self, name):
        if not os.path.isdir(name):
            os.makedirs(name)
        self.file_list.append(name)

    def select_folder(self, folder):
        os.chdir(folder)
        self.folder = os.getcwd()
        self.file_list = os.listdir(os.getcwd())

    def compress_image(self, multiplier=0, multiplier_x=0, multiplier_y=0):
        if multiplier and not (multiplier_x * multiplier_y):
            self.image = pygame.transform.scale(self.image, (self.image_size[0] / multiplier, self.image_size[1] / multiplier))
        elif not multiplier and multiplier_x * multiplier_y:
            self.image = pygame.transform.scale(self.image, (self.image_size[0] / multiplier_x, self.image_size[1] / multiplier_y))
        else:
            return
        pygame.image.save(self.image, self.image_name)

    def cut_images(self, name, *coordinates, folder=None):
        for (x, y), (x1, y1) in coordinates:
            clear_surface = pygame.Surface([x1 - x + 1, y1 - y + 1], pygame.SRCALPHA, 32)
            clear_surface.blit(self.image, (0, 0), (x, y, x1 + 1 ,y1 + 1))
            if folder:
                pygame.image.save(clear_surface, f'{self.folder}\\{folder}\\{name}_{self.counter}.png')
            else:
                pygame.image.save(clear_surface, f'{self.folder}\\{name}_{self.counter}.png')
            self.counter += 1
        self.counter = 0


if __name__ == '__main__':
    sheet = SpriteSheet('sprite.png')
    # sheet.make_directory('run')
    # sheet.cut_images('down_run', ((8, 6), (24, 30)), ((40, 5), (56, 31)), ((72, 6), (88, 30)), ((104, 5), (120, 31)), folder='run')
    # sheet.cut_images('left_run', ((9, 40), (24, 62)), ((41, 39), (56, 62)), ((73, 40), (88, 62)), ((105, 39), (120, 61)), folder='run')
    # sheet.cut_images('right_run', ((9, 72), (24, 94)), ((41, 71), (56, 94)), ((73, 72), (88, 94)), ((105, 71), (120, 93)), folder='run')
    # sheet.cut_images('up_run', ((8, 104), (24, 127)), ((40, 103), (56, 128)), ((72, 104), (88, 127)), ((104, 103), (120, 128)), folder='run')

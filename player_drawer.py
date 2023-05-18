import os, pygame

class PlayerDrawer:
    def __init__(self):
        self.x_position = 0
        self.y_position = 0
        self.side = 'down'
        self.sprites = {'left': [], 'right': [], 'up': [], 'down': []}
        self.status = 'worth'
        self.step_of_move = 10
        self.current_step = 0
        self.actions_in_frame = 5
        self.fps = 0

    def reading_sprites(self):
        dict_by_name = {'le': 'left', 'ri': 'right', 'up': 'up', 'do': 'down'}
        for image in os.listdir('run'):
            new_image = os.path.join('run', image)
            self.sprites[dict_by_name[image[:2]]].append(pygame.image.load(new_image))

    def choice_fps(self, meaning):
        self.fps = meaning

    def my_animation(self, game_screen, camera_position, frame):
        if self.status == 'worth':
            self.current_step = 0
            game_screen.blit(self.sprites[self.side][self.current_step], (camera_position[0], camera_position[1]))
        elif self.status == 'goes':
            if frame == 4:
                self.current_step = self.current_step + 1 if self.current_step + 1 < 4 else 1
            game_screen.blit(self.sprites[self.side][self.current_step], (camera_position[0], camera_position[1]))


    def move(self, keys):
        dba = {'K_a': ['-x', 'left', 'goes'], 'K_d': ['+x', 'right', 'goes'], 'K_w': ['-y', 'up', 'goes'], 'K_s': ['+y', 'down', 'goes'], False: 'worth'}
        if keys:
            dba_fs = {'x': self.x_position, 'y': self.y_position, '-': lambda a, b: a - b, '+': lambda a, b: a + b}
            for key_n in keys:
                if dba[key_n][0][1] == 'x':
                    self.x_position = dba_fs[dba[key_n][0][0]](dba_fs[dba[key_n][0][1]], self.step_of_move)
                elif dba[key_n][0][1] == 'y':
                    self.y_position = dba_fs[dba[key_n][0][0]](dba_fs[dba[key_n][0][1]], self.step_of_move)
                self.side = dba[key_n][1]
                self.status = dba[key_n][2]
        else:
            self.status = dba[keys]

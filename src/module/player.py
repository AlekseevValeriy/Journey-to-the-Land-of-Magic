from os import listdir

from pygame.image import load


class Player:
    def __init__(self, screen, position, person):
        self.screen = screen
        self.position: list = list(position)
        self.person = person
        self.step_on_30_frame_rate = 25
        self.present_step = self.step_on_30_frame_rate
        self.face_side = 'down'  # can be: down, up, left, right
        self.move_status = 'stand'  # can be: stand, run
        self.present_texture = 'down_run_0'
        self.textures = {}
        for image in listdir(f"../../data/textures/player/{self.person}"):
            self.textures[image.removesuffix('.png')] = load('/'.join([f"../../data/textures/player/{self.person}",
                                                                       image])).convert_alpha()

    def change_position(self, sign: int, axis: int):
        self.position[axis] = self.position[axis] + self.present_step * sign

    def change_step_under_frame_rate(self, frame_rate):
        self.present_step = (25 * 30) // frame_rate

    def get_position(self) -> list:
        return self.position

    def set_face_side(self, face_side: str):
        self.face_side = face_side


    def texture_selection(self):
        if self.move_status == 'stand':
            self.present_texture = f"{self.face_side}_run_0"
        elif self.move_status == 'run':
            self.present_texture = f"{self.face_side}_run_{(int(self.present_texture.split('_')[-1]) + 1) % 4}"

    def draw_player(self):
        self.texture_selection()
        texture = self.textures.get(self.present_texture, self.textures['up_run_0'])
        self.screen.blit(texture, [self.screen.get_width() // 2 - texture.get_width() // 2,
                                   self.screen.get_height() // 2 - texture.get_height() // 2])

    def player_move(self, status):
        self.move_status = status
        if self.move_status == 'run':
            if self.face_side == 'up':
                self.change_position(-1, 1)
            elif self.face_side == 'down':
                self.change_position(1, 1)
            elif self.face_side == 'left':
                self.change_position(-1, 0)
            elif self.face_side == 'right':
                self.change_position(1, 0)


if __name__ == '__main__':
    from pygame.display import set_mode

    p = Player(set_mode([1, 2]), 1)

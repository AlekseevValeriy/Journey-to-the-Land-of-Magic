from os import listdir

from pygame.image import load


class Player:
    def __init__(self, screen, position, person, **personal_data):
        self.personal_data = personal_data
        self.screen = screen
        self.position: list = list(position)
        self.person = person
        self.step_on_30_frame_rate = 12
        self.frame_skip_quality_on_30_frame_rate = 2
        self.frame_skip_quality = self.frame_skip_quality_on_30_frame_rate
        self.frame_skip = 0
        self.present_step = self.step_on_30_frame_rate
        self.face_side = 'down'  # can be: down, up, left, right
        self.move_status = 'stand'  # can be: stand, run
        self.present_texture = 'down_run_0'
        self.textures = {}
        for image in listdir(f"../../data/textures/player/{self.person}"):
            self.textures[image.removesuffix('.png')] = load('/'.join([f"../../data/textures/player/{self.person}",
                                                                       image])).convert_alpha()
        FRAME = 150
        self.run_frame_size = [FRAME, FRAME]
        self.run_frame_move = [0, 0]

    def get_personal_data(self):
        return self.personal_data

    def change_position(self, sign: int, axis: int):
        self.position[axis] = self.position[axis] + self.frame_inspector(axis, self.present_step * sign)

    def change_animation_under_fps(self, frame_rate):
        self.present_step = (self.step_on_30_frame_rate * 30) // frame_rate
        self.frame_skip_quality = (self.frame_skip_quality_on_30_frame_rate * frame_rate) // 30

    def get_frame(self):
        return self.run_frame_move

    def get_position(self) -> list:
        return self.position

    def set_face_side(self, face_side: str):
        self.face_side = face_side


    def texture_selection(self):
        if self.frame_skip != self.frame_skip_quality:
            self.frame_skip = (self.frame_skip + 1) % (self.frame_skip_quality + 1)
        else:
            self.frame_skip = 0
            if self.move_status == 'stand':
                self.present_texture = f"{self.face_side}_run_0"
            elif self.move_status == 'run':
                self.present_texture = f"{self.face_side}_run_{(int(self.present_texture.split('_')[-1]) + 1) % 4}"

    def draw_player(self):
        self.texture_selection()
        texture = self.textures.get(self.present_texture, self.textures['up_run_0'])
        self.screen.blit(texture, [(self.screen.get_width() // 2 + self.run_frame_move[0]) - texture.get_width() // 2,
                                   (self.screen.get_height() // 2 + self.run_frame_move[1]) - texture.get_height() // 2])

    def clear_frame_skip(self):
        self.frame_skip = 0

    def frame_inspector(self, axis, step):
        if ((step < 0 and self.run_frame_move[axis] > -self.run_frame_size[axis]) or
            (step > 0 and self.run_frame_move[axis] < self.run_frame_size[axis])):
            self.run_frame_move[axis] += step
            return 0
        return step

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

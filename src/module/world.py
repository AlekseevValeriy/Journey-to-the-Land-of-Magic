import numpy
from pygame.image import load


class World:
    def __init__(self, screen, world):
        self.screen = screen
        self.world: numpy.ndarray = world  # first layer is flagman, second layer is another..., last layer maybe objects
        self.world_sector_size = (100, 100)  # maybe a different size, I'll have more ideas in the final
        self.present_world: numpy.ndarray = numpy.array([])
        self.empty = load(f"../../data/textures/world/empty.png").convert_alpha()


    def screen_world_cut(self, player_position: list) -> tuple:
        screen_size = self.screen.get_size()
        row = player_position[0] // self.world_sector_size[0]
        col = player_position[1] // self.world_sector_size[1]
        scsi_row = screen_size[0] // self.world_sector_size[0]
        scsi_col = screen_size[1] // self.world_sector_size[1]
        l_r, r_r, u_c, d_c = 0, 2, 0, 2
        return (row + l_r, row + r_r + scsi_row), (col + u_c, col + d_c + scsi_col)

    def draw_world(self, player_position: list) -> None:
        draw_setting = self.screen_world_cut(player_position=player_position)
        for layer in self.world:
            for line in range(*draw_setting[1]):
                for element in range(*draw_setting[0]):
                    if 100 > line >= 0 and 100 > element >= 0:
                        self.screen.blit(layer[line][element], (element * self.world_sector_size[0] - player_position[0],
                                                                line * self.world_sector_size[1] - player_position[1]))
                    else:
                        self.screen.blit(self.empty,
                                         (element * self.world_sector_size[0] - player_position[0],
                                          line * self.world_sector_size[1] - player_position[1]))
import pygame
from sprite_sheet_maker import Spritesheet

# sheet = Spritesheet('sprite.png')
# sheet.make_directory('run_1')
# sheet.cut_images('down_run', 'run_1', ((8, 6), (24, 30)), ((40, 5), (56, 31)), ((72, 6), (88, 30)),
#                  ((104, 5), (120, 31)))
# sheet.cut_images('left_run', 'run_1', ((9, 40), (24, 62)), ((41, 39), (55, 62)), ((73, 40), (88, 62)),
#                  ((105, 40), (120, 61)))
# sheet.cut_images('right_run', 'run_1', ((9, 72), (24, 94)), ((41, 71), (56, 94)), ((73, 72), (88, 94)),
#                  ((105, 71), (120, 93)))
# sheet.cut_images('up_run', 'run_1', ((8, 104), (24, 127)), ((40, 103), (55, 128)), ((72, 104), (88, 127)),
#                  ((104, 103), (120, 128)))
# sprites = sheet.end()



background_colour = (234, 212, 252)
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('Geeksforgeeks')
screen.fill(background_colour)


sprite = pygame.image.load('ite.png')
# image = pygame.Surface([100, 100], pygame.SRCALPHA, 32)
# # image = image.convert_alpha()
# image.blit(sprite, (0, 0), (30, 30, 80 ,80))
# pygame.image.save(image, 'ite.png')
screen.blit(sprite, (0, 0))

pygame.display.flip()
running = True


# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
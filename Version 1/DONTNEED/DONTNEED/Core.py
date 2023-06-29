import random
import pygame

import map_generation

pygame.init()

with open('parameter.txt') as f:
    file = f.readlines()
    window = file[3].rstrip().lstrip('@').split('.')
    x_my, y_my = int(window[0]), int(window[1])
    map_new = file[5].rstrip().lstrip('@').split('.')
    map_x, map_y = int(map_new[0]), int(map_new[1])
    sector = map_new = file[7].rstrip().lstrip('@').split('.')
    sector_x, sector_y = int(sector[0]), int(sector[1])

pygame.font.init()
x_camera, y_camera, x_post, y_post = 0, 0, 500, 500
screen = pygame.display.set_mode((x_my, y_my))
color = (255, 100, 80)
level = map_generation.MapGeneration(map_x, map_y, [2, 4 ,8]).map_create()
individual_list = {}
end_point = False
for i in level:
    for j in i:
        if j not in individual_list:
            individual_list[j] = (random.randint(0, 255), random.randint(0, 255),
                                                                   random.randint(0, 255))
f1 = pygame.font.SysFont('Insight Sans SSi', 18)
fps = pygame.font.Font('fonts/Samson.ttf', 50)

def menu(pause):
    global end_point
    done = True
    color_1 = (255, 0, 0)
    color_2 = (0, 255, 0)
    while done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if event.button == 1 and 200 <= position[0] <= 300 and 125 <= position[1] <= 175:
                    done = False
                elif (event.button == 1 and 200 <= position[0] <= 300 and 250 <= position[1] <= 300) or (
                        event.type == pygame.QUIT):
                    done = False
                    pygame.quit()
                    end_point = True
                    break

            elif event.type == pygame.MOUSEMOTION:
                position = event.pos
                if 200 <= position[0] <= 300 and 125 <= position[1] <= 175:
                    color_1 = (255, 100, 0)
                else:
                    color_1 = (255, 0, 0)

                if 200 <= position[0] <= 300 and 250 <= position[1] <= 300:
                    color_2 = (100, 255, 100)
                else:
                    color_2 = (0, 255, 0)
        if end_point:
            break

        if pause:
            screen.fill((((255 + 150) // 2), ((255 + 150) // 2), ((255 + 150) // 2)))
            x = y = 0
            for row in level:
                for col in row:
                    color = individual_list[col]
                    new_color = ((individual_list[col][0] + 150) // 2,
                                 (individual_list[col][1] + 150) // 2,
                                 (individual_list[col][2] + 150) // 2)
                    pygame.draw.rect(screen, new_color, (x + x_camera, y + y_camera, 32, 48))
                    x += 32
                y += 48
                x = 0
            color = ((255 + 150) // 2, 150, 150)
            pygame.draw.rect(screen, color, (x_post * 0.8, y_post * 0.05, 70, 40))
            pygame.draw.rect(screen, ((255 + 150) // 2, 150, 150), (x_my // 2 + x_camera, y_my // 2 + y_camera, 10, 20))
        else:
            screen.fill((150, 150, 150))
        pygame.draw.rect(screen, color_1, (x_post // 2.5, y_post // 4, x_post * 0.2, y_post * 0.1))
        pygame.draw.rect(screen, color_2, (x_post // 2.5, y_post // 2, x_post * 0.2, y_post * 0.1))
        text1 = f1.render('Exit', True, (180, 0, 0))
        screen.blit(text1, (x_post // 2, y_post // 2))
        f2 = pygame.font.SysFont('Insight Sans SSi', 18)
        text2 = f2.render('Enter', True, (180, 0, 255))
        screen.blit(text2, (x_post // 2, y_post // 4))
        pygame.display.update()



clock = pygame.time.Clock()
game = True
speed_gorizontal = 0
speed_vertical = 0

FPS = 60
menu(False)
while game and not end_point:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            game = False
            end_point = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = event.pos
            if event.button == 1 and (x_post * 0.8 <= position[0] <= x_post * 0.8 + 70 and y_post * 0.05 <= position[
                1] <= y_post * 0.05 + 40):
                menu(True)
        elif event.type == pygame.MOUSEMOTION:
            position = event.pos
            if x_post * 0.8 <= position[0] <= x_post * 0.8 + 70 and y_post * 0.05 <= position[1] <= y_post * 0.05 + 40:
                color = (255, 100, 0)
            else:
                color = (255, 100, 80)
    if end_point:
        break
    keys = pygame.key.get_pressed()

    """move"""
    if keys[pygame.K_LEFT]:
        if speed_gorizontal != -3:
            speed_gorizontal -= 0.4
    if keys[pygame.K_RIGHT]:
        if speed_gorizontal != 3:
            speed_gorizontal += 0.4

    if keys[pygame.K_UP]:
        if speed_vertical != -3:
            speed_vertical -= 0.4
    if keys[pygame.K_DOWN]:
        if speed_vertical != 3:
            speed_vertical += 0.4

    """camera"""
    if keys[pygame.K_a]:
        x_camera += 5
    if keys[pygame.K_d]:
        x_camera -= 5

    if keys[pygame.K_w]:
        y_camera += 5
    if keys[pygame.K_s]:
        y_camera -= 5

    """exit"""
    if keys[pygame.K_x]:
        pygame.quit()
        game = False
        break

    """calculations"""
    x_my += speed_gorizontal
    y_my += speed_vertical
    if speed_gorizontal < 0:
        speed_gorizontal += 0.1
    elif speed_gorizontal > 0:
        speed_gorizontal -= 0.1

    if speed_vertical < 0:
        speed_vertical += 0.1
    elif speed_vertical > 0:
        speed_vertical -= 0.1

    """create"""
    screen.fill((255, 255, 255))
    x = y = 0
    for row in level:
        for col in row:
            pygame.draw.rect(screen, individual_list[col], (x + x_camera, y + y_camera, sector_x, sector_y))
            x += sector_x
        y += sector_y
        x = 0
    pygame.draw.rect(screen, color, (x_post * 0.8, y_post * 0.05, 70, 40))
    pygame.draw.rect(screen, (255, 0, 0), (x_my // 2 + x_camera, y_my // 2 + y_camera, 10, 20))

    text2 = fps.render(str(int(clock.get_fps())), True, (255, 0, 100))
    screen.blit(text2, (50, 50))

    pygame.display.update()

    clock.tick(FPS)

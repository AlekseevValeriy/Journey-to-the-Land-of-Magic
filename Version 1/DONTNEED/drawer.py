from PIL import Image, ImageDraw

def draw_map(colors_map, map_layout, wieght_image, hight_image):
    map_image = Image.new("RGB", (wieght_image, hight_image), (0, 0, 0))
    desk = ImageDraw.Draw(map_image)
    wieght_map, hight_map = len(map_layout), len(map_layout[0])
    sector_size = ((wieght_image + hight_image) // 2) // ((wieght_map + hight_map) // 2)
    for i in range(hight_map):
        for j in range(wieght_map):
            desk.rectangle((sector_size * j, sector_size * i, sector_size * (j + 1) - 1, sector_size * (i + 1) - 1),
                           fill=(colors_map[map_layout[i][j]]))

    map_image.save('Map_image.bmp')

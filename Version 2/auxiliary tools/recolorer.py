from PIL import Image
import os
os.chdir('..')
os.chdir('textures\\player\\Ash')
print(os.listdir())
print(os.getcwd())

for file in os.listdir():
    if file[-1] != '~':
        image = Image.open(file)
        pixels = image.load()
        x, y = image.size
        for i in range(y):
            for j in range(x):
                print(pixels[j, i])
                r, g, b, a = pixels[j, i]
                if r == 232 and g == 112 and b == 96:
                    pixels = (68, 68, 68, a)
                elif r == 176 and g == 80 and b == 72:
                    pixels = (0, 0, 0, a)
                elif r == 55 and g == 55 and b == 55:
                    pixels = (236, 11, 54, a)
                # elif r == 0 and g == 0 and b == 0:
                #     pixels = (149, 0, 28, a)
        image.save(file)
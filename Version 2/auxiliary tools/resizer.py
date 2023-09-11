from PIL import Image
from os import chdir, listdir

class Resizer:
    def __init__(self, multiple, *path):
        self.multiple = multiple
        [chdir(i) for i in path]

    def magnifier(self):
        for file in listdir():
            image = Image.open(file)
            x, y = image.size
            new_image = Image.new('RGBA', (x * self.multiple, y * self.multiple), (0, 0, 0, 0))
            new_mage = new_image.load()
            mage = image.load()
            for i in range(y):
                for j in range(x):
                    for h in range(self.multiple):
                        for t in range(self.multiple):
                            new_mage[j * self.multiple + h, i * self.multiple + t] = mage[j, i]
            new_image.save(file)

    def diminutive(self):
        # In future
        pass

if __name__ == '__main__':
    resizer = Resizer(3, '..', 'textures\\player\\Ashmax')
    resizer.magnifier()


from PIL import Image
from math import floor, ceil
from random import randrange
import timeit
# function input:
# number (integer) - number of pictures that the method should produce
# size (integer, odd) - size of the picture that the method should produce
# ratio (float in range from 0 to 1) - expected proportion of white-pixel pics to all produced pictures

class Matrix():

    def __init__(self, number, size, ratio):

        if type(number) is not int:
            raise TypeError('Number of cuts should be an integer!')
        if not size % 2:
            raise TypeError('Size of a slice should be an odd!')
        if 0 > ratio > 1 or type(ratio) is not float:
            raise TypeError('Ratio should be a float in range from 0 to 1!')
        if ratio - floor(number * ratio) / number > (ceil(number * ratio) / number) - ratio:
            self.white = ceil(number * ratio)
        else:
            self.white = floor(number * ratio)
        self.rgb = Image.open('rgb.png')
        self.distance = floor(size / 2)
        self.white_count = 0
        self.number = number
        self.collection = []
        self.classes = Image.open('classes.png')
        self.x, self.y = self.classes.size
        coord = self.get_coordinates()
        map(lambda x: self.crop(x), coord)

    def get_coordinates(self):
        x, y = randrange(0, self.x), randrange(0, self.y)
        if (x,y) not in self.collection:
            if self.white_count < self.white and self.classes.getpixel((x, y)) != 0:
                self.white_count += 1
                self.collection.append(f'{x}_{y}')
                return (x,y)
            elif len(self.collection) < self.number and self.classes.getpixel((x, y)) == 0:
                self.collection.append(f'{x}_{y}')
                return (x,y)
        else:
            self.get_coordinates()

    def crop(self, c):
        contour = (c[0] - self.distance, c[1] - self.distance,
                    c[0] + self.distance, c[1] + self.distance)
        file = open(f'{c[0]}_{c[1]}.png', 'w')
        self.rgb.crop(contour).save(file, "JPEG")


if __name__ == '__main__':
    import timeit
    print(timeit.timeit("Matrix(5, 85, 0.4)", setup="from __main__ import Matrix", number=1)
          )

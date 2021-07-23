from PIL import Image
from math import floor, ceil
from random import randrange
import timeit
# function input:
# number (integer) - number of pictures that the method should produce
# size (integer, odd) - size of the picture that the method should produce
# ratio (float in range from 0 to 1) - expected proportion of white-pixel pics to all produced pictures

def cut_pieces(number, size, ratio):

    classes_image = 'classes.png'
    rgb_image = 'rgb.png'

    # check input validity
    if type(number) is not int:
        raise TypeError('Number of cuts should be an integer!')
    if not size % 2:
        raise TypeError('Size of a slice should be an odd!')
    if 0 > ratio > 1 or type(ratio) is not float:
        raise TypeError('Ratio should be a float in range from 0 to 1!')

    calc = {}
    # calculate how many 'white-pixel' pics should be created. If ratio can't be matched accurately,
    # closest approximation is sought. When there are two possible ratios in equal distance from the original
    # one, program goes for greater number of white-pixel pics
    if ratio - floor(number * ratio) / number > (ceil(number * ratio) / number) - ratio:
        calc['white_num'] = ceil(number * ratio)
    else:
        calc['white_num'] = floor(number * ratio)
    calc['distance'] = floor(size / 2)
    m = Matrix(calc['white_num'], number)
    coord = [m.get_coordinates() for x in range(0, number)]
    pattern = Pattern(calc['distance'])
    coord = [pattern.crop(x) for x in coord]

class Pattern():

    def __init__(self, distance):
        self.rgb = Image.open('classes.png')
        self.distance = distance

    def crop(self, c):
        contour = (c[0] - self.distance, c[1] - self.distance,
                    c[0] + self.distance, c[1] + self.distance)
        self.rgb.crop(contour).save(open(f'{x}_{y}.png', 'r'), "JPEG")

class Matrix():
    def __init__(self, white, number):
        self.white = white
        self.white_count = 0
        self.number = number
        self.collection = []
        self.classes = Image.open('classes.png')
        self.x, self.y = self.classes.size

    def get_coordinates(self):
        x, y = randrange(0, self.x), randrange(0, self.y)
        if f'{x}_{y}' not in self.collection:
            if self.white_count < self.white and self.classes.getpixel((x, y)) != 0:
                self.white_count += 1
                self.collection.append(f'{x}_{y}')
                return (x,y)
            elif len(self.collection) < self.number and self.classes.getpixel((x, y)) == 0:
                self.collection.append(f'{x}_{y}')
                return (x,y)
        else:
            self.get_coordinates()

cut_pieces(11, 23, 0.5)
# if __name__ == '__main__':
#     import timeit
#     print(timeit.timeit("cut_pieces(5, 85, 0.4)", setup="from __main__ import cut_pieces", number=200)/200
#           )

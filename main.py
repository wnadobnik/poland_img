from PIL import Image
from math import floor, ceil
from random import randrange

# function input:
# number (interger) - number of pictures that the method should produce
# size (integer, odd) - size of the picture that the method should produce
# ratio (float in range from 0 to 1) - expected proportion of white-pixel pics to all produced pictures

def cut_pieces(number, size, ratio):

    classes_image = 'rgb.png'
    rgb_image = 'classes.png'

    # check input validity
    if type(number) is not int:
        raise TypeError('Number of cuts should be an integer!')
    if not size % 2:
        raise TypeError('Size of a slice should be an odd!')
    if 0 > ratio > 1 or type(ratio) is not float:
        raise TypeError('Ratio should be a float in range from 0 to 1!')

    previous = []

    calc = {}
    # calculate how many 'white-pixel' pics should be created. If ratio can't be matched accurately,
    # closest approximation is sought. When there are two possible ratios in equal distance from the original
    # one, program goes for greater number of white-pixel pics
    if ratio - floor(number * ratio) / number > (ceil(number * ratio) / number) - ratio:
        calc['white_num'] = ceil(number * ratio)
    else:
        calc['white_num'] = floor(number * ratio)
    calc['black_num'] = number - calc['white_num']
    calc['distance'] = floor(size / 2)
    calc['white_count'] = 0
    calc['black_count'] = 0

    with Image.open(classes_image) as classes:
        x_lim, y_lim = classes.size
        with Image.open(rgb_image) as rgb:
            calc['distance'] = floor(size / 2)
            while len(previous) < number:
                while True:
                    x, y = randrange(0, x_lim), randrange(0, y_lim)
                    if f'{x}_{y}' not in previous:
                        # check if pixel is white and if there are white-pixel pics left to produce
                        if calc['white_count'] < calc['white_num'] and classes.getpixel((x, y)) != 0:
                            calc['white_count'] += 1
                            outfile = open(f"test_{calc['white_count']}_w.png", 'w')
                            break
                        # check if pixel is black and if there are black-pixel pics left to produce
                        elif calc['black_count'] < calc['black_num'] and classes.getpixel((x, y)) == 0:
                            calc['black_count'] += 1
                            outfile = open(f"test_{calc['black_count']}_b.png", 'w')
                            break
                contour = (x - calc['distance'], y - calc['distance'],
                           x + calc['distance'], y + calc['distance'])
                rgb.crop(contour).save(outfile, "JPEG")
                previous.append(f'{x}_{y}')


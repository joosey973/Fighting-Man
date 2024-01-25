import os
import sys

import pygame


def load_image(path, color_key=None, is_reversed_x=False):
    fullname = os.path.join('data', path)
    if not os.path.isfile(fullname):
        print("Такого файла нет")
        print(fullname)
        sys.exit()
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    image = pygame.transform.flip(image, is_reversed_x, False)
    return image


def simple_load_image(path):
    img = pygame.image.load('data/' + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

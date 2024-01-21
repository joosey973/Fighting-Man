import os
import sys

import pygame


def load_image(path, color_key=None, is_reversed=False):
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
    if is_reversed:
        image = pygame.transform.flip(image, True, False)
    return image
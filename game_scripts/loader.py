import os
import pygame

def load_image_2(path):
    image = pygame.image.load('data/images/' + path).convert()
    image.set_colorkey((0, 0, 0))
    return image


def load_images(path):
    images = []
    for name in sorted(os.listdir('data/images/' + path)):
        images.append(load_image(path + '/' + name))
    return images
import json

from image_loader import load_image

import pygame


class Tilemap(pygame.sprite.Sprite):
    def __init__(self, ...):
        super().__init__(...)
        self.image = load_image(..., -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = ..., ...

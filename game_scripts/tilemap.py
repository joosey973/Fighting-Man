from image_loader import load_image

import pygame


class Tilemap(pygame.sprite.Sprite):
    def __init__(self, pos, type_of_tile, varint_of_tile, sprite_group):
        super().__init__(sprite_group)
        self.image = load_image(f"images/tiles/{type_of_tile}/{varint_of_tile}.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = list(map(lambda x: x + 500, pos))
        print(self.rect.x, self.rect.y, type_of_tile)
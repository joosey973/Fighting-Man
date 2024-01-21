from image_loader import load_image

import pygame


class Tilemap(pygame.sprite.Sprite):
    def __init__(self, pos, type_of_tile, varint_of_tile, sprite_group, all_sprites):
        super().__init__(sprite_group, all_sprites)
        size_tile = [16, 16]
        increase = 2.5
        self.image =  pygame.transform.scale(load_image(f"images/tiles/{type_of_tile}/{varint_of_tile}.png", -1), (size_tile[0] * increase, size_tile[1] * increase))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0] * (size_tile[0] * increase), pos[1] * (size_tile[1] * increase)
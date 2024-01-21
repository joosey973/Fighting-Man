from image_loader import load_image

import pygame


class Tilemap(pygame.sprite.Sprite):
    def __init__(self, pos, type_of_tile, varint_of_tile, tile_sprite_group, all_sprites):
        super().__init__(tile_sprite_group, all_sprites)
        self.tile_size = (16, 16)
        self.image = pygame.transform.scale(load_image(f"images/tiles/{type_of_tile}/{varint_of_tile}.png",
                                                       -1), (self.tile_size[0] * 2.4, self.tile_size[1] * 2.4))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 600, 530
        self.mask = pygame.mask.from_surface(self.image)

from image_loader import load_image

import pygame


class Tilemap(pygame.sprite.Sprite):
    def __init__(self, screen, pos, offset_x, offset_y, type_of_tile, varint_of_tile, tile_sprite_group, all_sprites):
        super().__init__(tile_sprite_group, all_sprites)
        self.screen = screen
        self.tile_size = (16, 16)
        self.image = pygame.transform.scale(load_image(f"images/tiles/{type_of_tile}/{varint_of_tile}.png",
                                                       -1), (self.tile_size[0] * 3, self.tile_size[1] * 3))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 600 + self.rect.width * offset_x, 530 + self.rect.height * -offset_y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)

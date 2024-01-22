from image_loader import load_image

import pygame


class Tilemap(pygame.sprite.Sprite):
    def __init__(self, calculation_of_coordinates, pos, type_of_tile, varint_of_tile,
                 sprite_group, other_sprite_group, all_sprites):
        if type_of_tile in ("grass", "stone"):
            super().__init__(sprite_group, all_sprites)
        else:
            super().__init__(other_sprite_group, all_sprites)
        if calculation_of_coordinates == 'tilemap':
            size_tile = [16, 16]
            increase = 2.5
            self.image = pygame.transform.scale(load_image(f"images/tiles/{type_of_tile}/{varint_of_tile}.png"),
                                                (size_tile[0] * increase, size_tile[1] * increase))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos[0] * (size_tile[0] * increase), pos[1] * (size_tile[1] * increase)
        if calculation_of_coordinates == 'offgrid':
            increase = 2.5
            if type_of_tile == 'decor':
                size_tile = [16, 16]
                self.image = pygame.transform.scale(load_image(
                    f"images/tiles/{type_of_tile}/{varint_of_tile}.png", -1), (size_tile[0] * increase, size_tile[1] * increase))
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = pos[0] / 16 * \
                    (size_tile[0] * increase), pos[1] / 16 * (size_tile[1] * increase)
            if type_of_tile == 'large_decor':
                size_tile = load_image(f"images/tiles/{type_of_tile}/{varint_of_tile}.png").get_rect().size
                # коэффициенты для расставление объектов на нужных местах
                a = size_tile[0] / 16
                b = size_tile[1] / 16
                self.image = pygame.transform.scale(load_image(
                    f"images/tiles/{type_of_tile}/{varint_of_tile}.png", -1), (size_tile[0] * increase, size_tile[1] * increase))
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = pos[0] / 16 * \
                    (size_tile[0] * increase / a), pos[1] / 16 * (size_tile[1] * increase / b)

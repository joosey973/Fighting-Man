from CharactersPhysics import Hero

from animations import Camera

from collide_system import Boarders

from image_loader import load_image

from outsiders_objects import Clouds, Particles

import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, screen, sprite, all_sprites):
        super().__init__(sprite, all_sprites)
        self.screen = screen
        self.size_block = [16, 16]
        self.image = pygame.transform.scale(load_image('images/tiles/grass/0.png'), (self.size_block[0] * 2, self.size_block[1] * 2))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.screen.get_width() // 2 + 100, self.screen.get_height() // 2 + 25

    # def platfoms(self):
    #     hero = Hero(self.screen, self.hero_sprite, self.all_sprites)
    #     if self.rect.collidepoint():
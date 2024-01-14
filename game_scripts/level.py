from CharactersPhysics import Hero

from animations import Camera

from collide_system import Boarders

from image_loader import load_image

from outsiders_objects import Clouds, Particles

import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, screen, width, height, sprite, all_sprites):
        super().__init__(sprite, all_sprites)
        self.width = width
        self.height = height
        self.screen = screen
        self.size_block = [16, 16]
        self.block = pygame.transform.scale(load_image('images/tiles/grass/0.png'), (self.size_block[0] * 2, self.size_block[1] * 2))
        self.block_rect = self.block.get_rect()
        self.block_rect.x, self.block_rect.y = self.width // 2 + 100, self.height // 2 + 25

    # def platfoms(self):
    #     hero = Hero(self.screen, self.hero_sprite, self.all_sprites)
    #     if self.block_rect.collidepoint():
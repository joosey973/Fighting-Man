import random

from image_loader import load_image

import pygame


class Particles(pygame.sprite.Sprite):
    def __init__(self, screen, particle, particles_sprite):
        super().__init__(particles_sprite)
        self.screen = screen
        self.particle = particle
        self.ind_of_particle = 0
        self.index = 0
        self.image = pygame.transform.scale(load_image(f"images/particles/{self.particle}/{self.ind_of_particle}.png",
                                                       -1), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.rect.width, self.screen.get_width() - self.rect.width + 1)
        self.rect.y = random.randrange(self.rect.height, self.screen.get_height() - self.rect.height + 1)

    def update(self):
        self.image = pygame.transform.scale(load_image(f"images/particles/{self.particle}/{self.ind_of_particle}.png",
                                                       -1), (20, 20))
        if self.index == 20:
            self.ind_of_particle += 1
            self.index = 0
        if self.particle == "leaf" and self.ind_of_particle == 17:
            self.ind_of_particle = 0
            self.index = 0
        elif self.particle == "particle" and self.ind_of_particle == 3:
            self.ind_of_particle = 0
            self.index = 0
        self.index += 1
        self.rect = self.rect.move(0, 1)

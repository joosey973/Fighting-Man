import random

from image_loader import load_image

import pygame


class Particles(pygame.sprite.Sprite):
    def __init__(self, screen, particle, particles_sprite, horizontal_borders, all_sprites):
        super().__init__(particles_sprite, all_sprites)
        self.screen = screen
        self.particle = particle
        self.horizontal_borders = horizontal_borders
        self.ind_of_particle, self.index = 0, 0
        self.image = pygame.transform.scale(load_image(f"images/particles/{self.particle}/{self.ind_of_particle}.png",
                                                       -1), (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.rect.width, self.screen.get_width() - self.rect.width + 1)
        self.rect.y = random.randrange(self.rect.height, self.screen.get_height() - self.rect.height + 1)

    def update(self):
        if pygame.sprite.spritecollideany(self, self.horizontal_borders):
            self.kill()
        self.image = pygame.transform.scale(load_image(f"images/particles/{self.particle}/{self.ind_of_particle}.png",
                                                       -1), (16, 16))
        if self.index == 3:
            self.ind_of_particle += 1
            self.index = 0
        if self.particle == "leaf" and self.ind_of_particle == 17:
            self.ind_of_particle = 0
            self.index = 0
        self.index += 1
        self.rect = self.rect.move(0, 1)


class Clouds(pygame.sprite.Sprite):
    clouds_list = []

    def __init__(self, screen, clouds_sprites, all_sprites):
        super().__init__(clouds_sprites, all_sprites)
        self.screen = screen
        self.image = load_image(f"images/clouds/cloud_{random.randint(1, 2)}.png", -1)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width * 3, self.rect.height * 3))
        self.rect = self.image.get_rect()
        Clouds.clouds_list.append(self.rect)
        self.generate_clouds()

    def generate_clouds(self):
        self.rect.x = random.randrange(self.rect.width // 3, self.screen.get_width() - self.rect.width // 3 + 1)
        self.rect.y = random.randrange(self.rect.height // 3, self.screen.get_height() - self.rect.height + 1)
        new_list_of_clouds_loc = Clouds.clouds_list.copy()
        new_list_of_clouds_loc.remove(self.rect)
        while self.rect.collidelistall(new_list_of_clouds_loc):
            self.rect.x = random.randrange(self.rect.width // 3, self.screen.get_width() - self.rect.width // 3 + 1)
            self.rect.y = random.randrange(self.rect.height // 3, self.screen.get_height() - self.rect.height + 1)

    def update(self):
        if self.rect.right <= 0:
            self.rect.left = self.screen.get_width()
        elif self.rect.left >= self.screen.get_width():
            self.rect.right = 0
        self.rect = self.rect.move(1, 0)

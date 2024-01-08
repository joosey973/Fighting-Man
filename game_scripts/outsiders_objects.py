import random

from image_loader import load_image

import pygame


class Particles(pygame.sprite.Sprite):
    def __init__(self, screen, particle, particles_sprite, all_sprites):
        super().__init__(particles_sprite)
        self.screen = screen
        self.particle = particle
        self.all_sprites = all_sprites
        self.ind_of_particle = 0
        self.index = 0
        self.image = pygame.transform.scale(load_image(f"images/particles/{self.particle}/{self.ind_of_particle}.png",
                                                       -1), (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.rect.width, self.screen.get_width() - self.rect.width + 1)
        self.rect.y = random.randrange(self.rect.height, self.screen.get_height() - self.rect.height + 1)

    def update(self):
        if pygame.sprite.spritecollideany(self, self.all_sprites):
            self.kill()
        self.image = pygame.transform.scale(load_image(f"images/particles/{self.particle}/{self.ind_of_particle}.png",
                                                       -1), (16, 16))
        if self.index == 1:
            self.ind_of_particle += 1
            self.index = 0
        if self.particle == "leaf" and self.ind_of_particle == 17:
            self.ind_of_particle = 0
            self.index = 0
        self.index += 1
        self.rect = self.rect.move(0, 1)


class Clouds(pygame.sprite.Sprite):
    clouds_list = []

    def __init__(self, screen, ind_of_cloud, clouds_sprites, all_sprites):
        super().__init__(clouds_sprites)
        self.screen = screen
        self.all_sprites = all_sprites
        self.image = load_image(f"images/clouds/cloud_{ind_of_cloud}.png", -1)
        self.rect = self.image.get_rect()
        self.rect.width *= 3
        self.rect.height *= 3
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.rect = self.image.get_rect()
        Clouds.clouds_list.append(self.rect)
        self.spawn_clouds()

    def spawn_clouds(self):
        self.rect.x = random.randrange(self.rect.width // 3, self.screen.get_width() - self.rect.width // 3 + 1)
        self.rect.y = random.randrange(self.rect.height // 3, self.screen.get_height() - self.rect.height + 1)
        new_list_of_clouds_loc = Clouds.clouds_list.copy()
        new_list_of_clouds_loc.remove(self.rect)
        while self.rect.collidelistall(new_list_of_clouds_loc):
            self.rect.x = random.randrange(self.rect.width // 3, self.screen.get_width() - self.rect.width // 3 + 1)
            self.rect.y = random.randrange(self.rect.height // 3, self.screen.get_height() - self.rect.height + 1)

    def update(self):
        if pygame.sprite.spritecollideany(self, self.all_sprites):
            self.rect.x = self.rect.width // 8
        self.rect = self.rect.move(1, 0)

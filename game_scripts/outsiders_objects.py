import random

from animations import particles_animation

from image_loader import load_image

import pygame


class Particles(pygame.sprite.Sprite):
    def __init__(self, screen, particle, particles_sprite, horizontal_borders, vertical_borders, all_sprites):
        super().__init__(particles_sprite, all_sprites)
        self.screen = screen
        self.particle = particle
        self.horizontal_borders = horizontal_borders
        self.vertical_borders = vertical_borders
        self.image = particles_animation("images/particles/leaf/{}.png", "leaf", 17, (8, 8), 2)
        self.rect = self.image.get_rect()
        self.__set_start_coord()
        self.time_count = 0
        self.offset_x = [-1, 1][random.randrange(2)]

    def __set_start_coord(self):
        self.rect.x = random.randrange(self.rect.width, self.screen.get_width() - self.rect.width + 1)
        self.rect.y = random.randrange(self.rect.height, self.screen.get_height() - self.rect.height + 1)

    def update(self, is_update=False):
        if pygame.sprite.spritecollideany(self, self.vertical_borders):
            self.kill()
        if pygame.sprite.spritecollideany(self, self.horizontal_borders):
            self.kill()
        self.image = particles_animation("images/particles/leaf/{}.png", "leaf", 17, (8, 8), 2)
        if is_update:
            self.rect = self.rect.move(self.offset_x, 1)
        if self.time_count == 50:
            self.time_count = 0
            self.offset_x = -self.offset_x
        self.time_count += 1


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
        self.rect.x = random.randrange(self.rect.width, self.screen.get_width() - self.rect.width) - \
            self.screen.get_width() // 4
        self.rect.y = random.randrange(self.rect.height, self.screen.get_height() - self.rect.height)
        new_list_of_clouds_loc = Clouds.clouds_list.copy()
        new_list_of_clouds_loc.remove(self.rect)
        while self.rect.collidelistall(new_list_of_clouds_loc):
            self.rect.x = random.randrange(self.rect.width, self.screen.get_width() - self.rect.width) - \
                self.screen.get_width() // 4
            self.rect.y = random.randrange(self.rect.height, self.screen.get_height() - self.rect.height)

    def update(self, is_update=False):
        if is_update:
            self.rect.right += 1
        if self.rect.right <= 0:
            self.rect.left = self.screen.get_width()
        elif self.rect.left >= self.screen.get_width():
            self.rect.right = 0
        if self.rect.top >= self.screen.get_height():
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = self.screen.get_height()


class Particle(pygame.sprite.Sprite):
    def __init__(self, particle_sprite, hero_pos, is_flight, screen, velocities):
        super().__init__(particle_sprite)
        self.is_flight = is_flight
        self.screen = screen
        self.image = pygame.transform.scale(load_image(f"images/particles/particle/{random.randrange(0, 3)}.png", -1),
                                            (33, 33))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = hero_pos
        self.dx, self.dy = velocities

    def update(self):
        if (self.rect.left >= self.screen.get_width() or self.rect.right <= 0 or
                self.rect.top >= self.screen.get_height() or self.rect.bottom <= 0):
            self.is_flight = True
            self.kill()
        self.rect.x += self.dx
        self.rect.y += self.dy

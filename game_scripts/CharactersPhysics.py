from image_loader import load_image

import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, screen, sprite):
        super().__init__(sprite)
        self.screen = screen
        self.index_of_hero_static_img = 0
        self.index_0 = 0
        self.index_of_hero_running_img = 0
        self.index_1 = 0
        self.image = pygame.transform.scale(load_image(f"images/entities/player/idle/"
                                                       f"{self.index_of_hero_static_img}.png", -1), (70, 90))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 300
        self.is_left = False
        self.dx = 1
        self.dy = 1

    def do_the_running_animation(self, is_reversed=False):
        self.is_left = is_reversed
        self.index_0, self.index_of_hero_static_img = 0, 0
        self.image = pygame.transform.scale(load_image(f"images/entities/player/run/"
                                            f"{self.index_of_hero_running_img}.png", -1, is_reversed), (70, 90))
        if self.index_1 == 20:
            self.index_of_hero_running_img += 1
            self.index_1 = 0
        if self.index_of_hero_running_img == 7:
            self.index_of_hero_running_img = 0
        self.index_1 += 1

    def do_the_static_animation(self, is_reversed=False):
        self.index_1, self.index_of_hero_running_img = 0, 0
        self.image = pygame.transform.scale(load_image(f"images/entities/player/idle/"
                                            f"{self.index_of_hero_static_img}.png", -1, is_reversed), (70, 90))
        if self.index_0 == 20:
            self.index_of_hero_static_img += 1
            self.index_0 = 0
        if self.index_of_hero_static_img == 21:
            self.index_of_hero_static_img = 0
        self.index_0 += 1

    def do_rotate(self, key):
        if key[pygame.K_d] and self.dx + self.rect.right < self.screen.get_width():
            self.do_the_running_animation()
            self.rect.right += self.dx
        elif key[pygame.K_a] and self.rect.left - self.dx > 0:
            self.do_the_running_animation(is_reversed=True)
            self.rect.left -= self.dx
        elif key[pygame.K_w] and self.rect.top - self.dy > 0:
            self.do_the_running_animation()
            self.rect.top -= self.dy
        else:
            if self.is_left is True:
                self.do_the_static_animation(is_reversed=True)
            else:
                self.do_the_static_animation()

    def update(self, key):
        self.do_rotate(key)

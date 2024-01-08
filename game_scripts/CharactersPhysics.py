from image_loader import load_image

import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, screen, sprite):
        super().__init__(sprite)
        self.screen = screen
        self.index_of_hero_static_img, self.index_0 = 0, 0
        self.index_of_hero_running_img, self.index_1 = 0, 0
        self.hero_sizes = (14, 18)
        self.image = pygame.transform.scale(load_image(f"images/entities/player/idle/"
                                                       f"{self.index_of_hero_static_img}.png", -1),
                                            (self.hero_sizes[0] * 3.5, self.hero_sizes[1] * 3.5))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 300
        self.is_left = False
        self.jump_mode = 2  # 0 - в прыжке, 1 - падает, 2 - не прыгает
        self.jump_counter = 0  # счетчик подъема/спуска
        self.is_jump = False
        self.dx = 1
        self.dy = 1

    def do_the_running_animation(self, is_reversed=False):
        self.is_left = is_reversed
        self.index_0, self.index_of_hero_static_img = 0, 0
        self.image = pygame.transform.scale(load_image(f"images/entities/player/run/"
                                            f"{self.index_of_hero_running_img}.png", -1, is_reversed),
                                            (self.hero_sizes[0] * 3.5, self.hero_sizes[1] * 3.5))
        if self.index_1 == 20:
            self.index_of_hero_running_img += 1
            self.index_1 = 0
        if self.index_of_hero_running_img == 7:
            self.index_of_hero_running_img = 0
        self.index_1 += 1

    def do_the_static_animation(self, is_reversed=False):
        self.index_1, self.index_of_hero_running_img = 0, 0
        self.image = pygame.transform.scale(load_image(f"images/entities/player/idle/"
                                            f"{self.index_of_hero_static_img}.png", -1, is_reversed),
                                            (self.hero_sizes[0] * 3.5, self.hero_sizes[1] * 3.5))
        if self.index_0 == 20:
            self.index_of_hero_static_img += 1
            self.index_0 = 0
        if self.index_of_hero_static_img == 21:
            self.index_of_hero_static_img = 0
        self.index_0 += 1

    def do_the_jumping_animation(self, is_reversed=False):
        self.is_left = is_reversed
        self.index_0, self.index_of_hero_static_img, \
            self.index_1, self.index_of_hero_running_img = (0 for _ in range(4))
        self.image = pygame.transform.scale(load_image("images/entities/player/jump/0.png", -1, is_reversed),
                                            (self.hero_sizes[0] * 3.5, self.hero_sizes[1] * 3.5))

    def do_jump(self):
        if self.jump_mode == 0 and self.jump_counter <= 50:
            self.do_the_jumping_animation(self.is_left)
            self.rect.top -= self.dy
            self.jump_counter += self.dy
        if self.jump_counter == 50:
            self.jump_mode = 1
        if self.jump_mode == 1 and self.jump_counter >= 0:
            self.do_the_jumping_animation(self.is_left)
            self.rect.bottom += self.dy
            self.jump_counter -= self.dy
        if self.jump_counter == 0:
            self.jump_mode = 2
            self.is_jump = False

    def do_rotate(self, key):
        if key[pygame.K_w] and self.rect.top - self.dy > 0 and not self.is_jump:
            self.jump_mode = 0
            self.is_jump = True
        elif key[pygame.K_a] and self.rect.left - self.dx > 0:
            self.do_the_running_animation(is_reversed=True)
            self.rect.left -= self.dx
        elif key[pygame.K_d] and self.dx + self.rect.right < self.screen.get_width():
            self.do_the_running_animation()
            self.rect.right += self.dx
        else:
            if self.is_left is True:
                self.do_the_static_animation(is_reversed=True)
            else:
                self.do_the_static_animation()
        self.do_jump()

    def update(self, key):
        self.do_rotate(key)


# TODO: пофиксить баг с прыжком, добавить анимацию прыжка

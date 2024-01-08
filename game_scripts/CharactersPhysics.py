from image_loader import load_image

import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, screen, sprite):
        super().__init__(sprite)
        self.screen = screen
        self.hero_sizes = (14, 18)
        self.index_of_hero_pos, self.index = 0, 0
        self.type_of_pos = None
        self.image = pygame.transform.scale(load_image("images/entities/player/idle/0.png", -1), (self.hero_sizes[0] * 3, self.hero_sizes[1] * 3))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 300
        self.is_left = False
        self.jump_mode = 2  # 0 - в прыжке, 1 - падает, 2 - не прыгает
        self.jump_counter = 0  # счетчик подъема/спуска
        self.is_jump = False
        self.dx = 3
        self.dy = 3

    def func(self, type_of_move):
        if self.type_of_pos != type_of_move:
            self.type_of_pos = type_of_move
            self.index_of_hero_pos, self.index = 0, 0
        self.image = pygame.transform.scale(load_image(f"images/entities/player/{type_of_move}/"
                                                       f"{self.index_of_hero_pos}.png", -1, self.is_left),
                                            (self.hero_sizes[0] * 3, self.hero_sizes[1] * 3))
        if self.index == 5:
            self.index_of_hero_pos += 1
            self.index = 0
        if type_of_move == "idle" and self.index_of_hero_pos == 21:
            self.index_of_hero_pos = 0
        if type_of_move == "run" and self.index_of_hero_pos == 7:
            self.index_of_hero_pos = 0
        if type_of_move == "jump" and self.index_of_hero_pos == 1:
            self.index_of_hero_pos = 0
        if type_of_move == "slide" and self.index_of_hero_pos == 1:
            self.index_of_hero_pos = 0
        self.index += 1

    def do_jump(self):
        if self.jump_mode == 0 and self.jump_counter < 60:
            self.func("jump")
            self.jump_counter += self.dy
            self.rect.top -= self.dy
        if self.jump_counter == 60:
            self.jump_mode = 1
        if self.jump_mode == 1 and self.jump_counter > 0:
            self.func("jump")
            self.jump_counter -= self.dy
            self.rect.bottom += self.dy
        if self.jump_counter == 0:
            self.is_jump = False
            self.jump_counter = 0
            self.jump_mode = 2

    def do_rotate(self, key):
        if (key[pygame.K_w] and self.rect.top - self.dy > 0 and not self.is_jump or
                key[pygame.K_SPACE] and self.rect.top - self.dy > 0) and not self.is_jump:
            self.is_jump = True
            self.jump_mode = 0
        elif key[pygame.K_a] and self.rect.left - self.dx > 0:
            self.is_left = True
            self.func("run")
            self.rect.left -= self.dx
        elif key[pygame.K_d] and self.rect.right + self.dx < self.screen.get_width():
            self.is_left = False
            self.func("run")
            self.rect.right += self.dx
        else:
            self.func("idle")
        self.do_jump()

    def update(self, key):
        self.do_rotate(key)

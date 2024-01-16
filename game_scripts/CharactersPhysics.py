from animations import entities_animations

from image_loader import load_image

import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, screen, sprite, all_sprites):
        super().__init__(sprite, all_sprites)
        self.index_of_hero_pos, self.index = 0, 0
        self.screen = screen
        self.hero_sizes = (14, 18)
        self.is_left = False
        self.is_jump = False
        self.jump_height = 16
        self.FPS = 60
        self.dx, self.dy = 100, self.jump_height
        self.gravity = 1
        self.slide_limit = 0  # лимит будет в 5 пикселей
        self.image = pygame.transform.scale(load_image("images/entities/player/idle/0.png", -1),
                                            (self.hero_sizes[0] * 3, self.hero_sizes[1] * 3))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, 500

    def do_jump(self):
        if self.jump_mode == 0 and self.jump_counter < 50:
            self.image = entities_animations("images/entities/player/jump/{}.png", "jump", 1, (14, 18), 3, self.is_left)
            self.jump_counter += self.dy
            self.rect.top -= self.dy
        if self.jump_counter == 50:
            self.jump_mode = 1
        if self.jump_mode == 1 and self.jump_counter > 0:
            self.image = entities_animations("images/entities/player/jump/{}.png", "jump", 1, (14, 18), 3, self.is_left)
            self.jump_counter -= self.dy
            self.rect.bottom += self.dy
        if self.jump_counter == 0:
            self.is_jump = False
            self.jump_counter = 0
            self.jump_mode = 2

    def do_rotate(self, key):
        if (key[pygame.K_w] or key[pygame.K_SPACE]):
            self.is_jump = True
        if self.is_jump:
            self.rect.bottom -= self.dy
            self.dy -= self.gravity
            self.image = entities_animations("images/entities/player/jump/{}.png", "jump", 1, (14, 18), 3, self.is_left)
            if self.dy < -self.jump_height:
                self.is_jump = False
                self.dy = self.jump_height
                self.image = entities_animations("images/entities/player/jump/{}.png", "jump", 1, (14, 18),
                                                 3, self.is_left)
        if key[pygame.K_d]:
            self.is_left = False
            if not self.is_jump:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 3, self.is_left)
            self.rect.right += self.dx / self.FPS
        elif key[pygame.K_a]:
            self.is_left = True
            if not self.is_jump:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 3, self.is_left)
            self.rect.left -= self.dx / self.FPS
        else:
            if not self.is_jump:
                self.image = entities_animations("images/entities/player/idle/{}.png", "idle", 21, (14, 18), 3,
                                                 self.is_left)

    def update(self):
        key = pygame.key.get_pressed()
        self.do_rotate(key)

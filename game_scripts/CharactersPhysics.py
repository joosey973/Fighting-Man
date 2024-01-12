from animations import entities_animations

from image_loader import load_image

import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, screen, sprite, all_sprites):
        super().__init__(sprite, all_sprites)
        self.index_of_hero_pos, self.index = 0, 0
        self.screen = screen
        self.hero_sizes = (14, 18)
        self.type_of_pos = None
        self.jump_counter = 0  # счетчик подъема/спуска
        self.jump_mode = 2  # 0 - в прыжке, 1 - падает, 2 - не прыгает
        self.is_left = False
        self.is_jump = False
        self.is_slide = False
        self.dx, self.dy = 5, 5
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

        if (key[pygame.K_w] and self.rect.top - self.dy > 0 and not self.is_jump or
                key[pygame.K_SPACE] and self.rect.top - self.dy > 0) and not self.is_jump:
            self.is_slide = False
            self.is_jump = True
            self.jump_mode = 0
        elif (key[pygame.K_s] and self.rect.top - self.dy > 0 and not self.is_jump or
                key[pygame.K_LCTRL] and self.rect.top - self.dy < self.screen.get_height()):
            self.image = entities_animations("images/entities/player/slide/{}.png", "slide", 1, (14, 18), 3,
                                             self.is_left)
            if self.is_left and self.slide_limit > -250:
                self.is_slide = True
                self.rect.left -= self.dx * 4
                self.slide_limit -= self.dx * 4
            elif not self.is_left and self.slide_limit < 250:
                self.is_slide = True
                self.rect.right += self.dx * 4
                self.slide_limit += self.dx * 4
        elif self.is_slide and (self.slide_limit == 250 or self.slide_limit == -250):
            self.slide_limit = 0
            self.is_slide = False
        elif key[pygame.K_a] and self.rect.left - self.dx > 0:
            self.is_slide = False
            self.is_left = True
            self.image = entities_animations("images/entities/player/run/{}.png", "run", 7, (14, 18), 3, self.is_left)
            self.rect.left -= self.dx
        elif key[pygame.K_d] and self.rect.right + self.dx < self.screen.get_width():
            self.is_slide = False
            self.is_left = False
            self.image = entities_animations("images/entities/player/run/{}.png", "run", 7, (14, 18), 3, self.is_left)
            self.rect.right += self.dx
        else:
            self.is_slide = False
            self.image = entities_animations("images/entities/player/idle/{}.png", "idle", 21, (14, 18), 3,
                                             self.is_left)
        if not self.is_slide:
            self.slide_limit = 0
        self.do_jump()

    def update(self):
        key = pygame.key.get_pressed()
        self.do_rotate(key)

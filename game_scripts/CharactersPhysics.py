from animations import entities_animations

from image_loader import load_image

from outsiders_objects import Particle

import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, screen, sprite, all_sprites, tile_sprites):
        super().__init__(sprite, all_sprites)
        self.tile_sprites = tile_sprites
        self.particle_sprite_group = pygame.sprite.Group()
        self.screen = screen
        self.hero_sizes = (14, 18)
        self.is_left = False
        # --- Все для слайда
        self.is_slide = False
        self.slide_count = 0
        # ---
        # --- Для прыжка и движения по горизонтали
        self.is_drop = True
        self.vel_y = 0
        self.is_jumping = False
        self.gravity = 1
        self.dx, self.dy = 0, 0
        # --- Инициализация картинки, объявления хитбокса и положения относительно экрана
        self.image = pygame.transform.scale(load_image("images/entities/player/idle/0.png", -1),
                                            (self.hero_sizes[0] * 4, self.hero_sizes[1] * 4))
        self.rect = self.image.get_rect()
        # self.rect.width //= 2
        self.rect.x, self.rect.y = 700, 0

    # Функция для прыжка

    def do_jump(self):
        self.vel_y += self.gravity
        if self.vel_y > 20:
            self.vel_y = 20
        self.dy += self.vel_y
        self.image = entities_animations("images/entities/player/jump/{}.png",
                                         "jump", 1, (14, 18), 4, self.is_left)

    # Физика и анимация слайда
    def do_slide(self):
        if self.is_slide:
            self.rect.x = self.rect.x + 5 if not self.is_left else self.rect.x - 5
            self.slide_count += 1
        if self.slide_count >= 60:
            self.slide_count = 0
            self.is_slide = False
            [Particle(self.particle_sprite_group, (self.rect.x, self.rect.y), self.is_left) for i in range(20)]

    def do_horizontal_and_static_move(self, key):
        if key[pygame.K_d]:
            self.is_left = False
            if not self.is_jumping:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 4, self.is_left)
            self.dx += 2

        elif key[pygame.K_a]:
            self.is_left = True
            if not self.is_jumping:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 4, self.is_left)
            self.dx -= 2

        else:
            if not self.is_jumping:
                self.image = entities_animations("images/entities/player/idle/{}.png", "idle",
                                                 21, (14, 18), 4,
                                                 self.is_left)

    # Функция для отработки движения персонажа
    def do_rotate(self, event):
        key = pygame.key.get_pressed()
        self.dx, self.dy = 0, 0

        if event is not None and event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or key[pygame.K_SPACE]):
                self.is_jumping = True
                self.vel_y = -20

            if event.key == pygame.K_LSHIFT:
                self.image = pygame.transform.scale(load_image("images/particles/particle/0.png",
                                                               -1), (25, 25))
                self.is_slide = True



        self.do_slide()
        if self.is_slide:
            return
        # Физика и анимация прыжка
        if self.is_jumping:
            self.do_jump()
        # Физика и анимация движения по горизонтали и статического положения
        self.do_horizontal_and_static_move(key)

        if self.particle_sprite_group:  # Если есть спрайты в спрайт-группе
            self.particle_sprite_group.update()
            self.particle_sprite_group.draw(self.screen)

        for tile in self.tile_sprites:

            if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.rect.bottom < tile.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = tile.rect.top - 5
                        self.dy = 0
                        self.vel_y = 0
                        self.is_jumping = False
                elif self.rect.top > tile.rect.centery:
                    self.rect.top = tile.rect.bottom + 3
            # if (not tile.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height) or not tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height)) and not self.is_jumping:
            #     self.dy = 10
            if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                self.dx = 0

        self.rect.x += self.dx
        self.rect.y += self.dy

    def update(self, event=None):
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        self.do_rotate(event)

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
        self.jump_height = 17
        self.is_jump = False
        self.dx, self.dy = 0, self.jump_height
        # --- Инициализация картинки, объявления хитбокса и положения относительно экрана
        self.image = pygame.transform.scale(load_image("images/entities/player/idle/0.png", -1),
                                            (self.hero_sizes[0] * 3, self.hero_sizes[1] * 3))
        self.rect = self.image.get_rect()
        self.rect.width //= 1.25
        self.rect.x, self.rect.y = self.screen.get_width() // 2, self.screen.get_height() // 2

    # Функция для прыжка

    def do_jump(self):
        self.rect.bottom -= self.dy
        self.dy -= 2
        self.image = entities_animations("images/entities/player/jump/{}.png",
                                         "jump", 1, (14, 18), 3, self.is_left)
        if self.dy < -self.jump_height:
            self.dy = self.jump_height
            self.is_jump = False

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
            if not self.is_jump:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 3, self.is_left)
            self.dx = 2

        elif key[pygame.K_a]:
            self.is_left = True
            if not self.is_jump:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 3, self.is_left)
            self.dx = -2

        else:
            if not self.is_jump:
                self.image = entities_animations("images/entities/player/idle/{}.png", "idle",
                                                 21, (14, 18), 3,
                                                 self.is_left)

    # Функция для отработки движения персонажа
    def do_rotate(self, event):
        for rect in self.tile_sprites:
            if rect.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                self.dx = 0


        key = pygame.key.get_pressed()
        if event is not None and event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or key[pygame.K_SPACE]):
                self.is_jump = True
            if event.key == pygame.K_LSHIFT:
                self.image = pygame.transform.scale(load_image("images/particles/particle/0.png",
                                                               -1), (25, 25))
                self.is_slide = True
        self.do_slide()
        if self.is_slide:
            return

        # Физика и анимация прыжка
        if self.is_jump:
            self.do_jump()
        # Физика и анимация движения по горизонтали и статического положения
        self.do_horizontal_and_static_move(key)

        if self.particle_sprite_group:  # Если есть спрайты в спрайт-группе
            self.particle_sprite_group.update()
            self.particle_sprite_group.draw(self.screen)
        self.rect = self.rect.move(self.dx, 0)
        self.dx = 0

    def update(self, event=None):
        self.do_rotate(event)

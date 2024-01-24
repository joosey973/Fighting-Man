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
        self.is_flight = True
        # --- Для прыжка и движения по горизонтали
        self.jumps = 2
        self.vel_y = 0
        self.is_jumping = False
        self.gravity = 0.8
        self.dx, self.dy = 0, 0
        # --- Для дэша персонажа
        self.is_dash = False
        self.dash_count = 0

        # --- Инициализация картинки, объявления хитбокса и положения относительно экрана
        self.image = pygame.transform.scale(load_image("images/entities/player/idle/0.png", -1),
                                            (self.hero_sizes[0] * 4, self.hero_sizes[1] * 4))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.screen.get_width() // 2, self.screen.get_height() // 2
        if self.particle_sprite_group:  # Если есть спрайты в спрайт-группе
            self.particle_sprite_group.update()
            self.particle_sprite_group.draw(self.screen)


    # Физика и анимация слайда
    def do_slide(self):
        if self.is_slide:
            self.image = pygame.transform.scale(load_image("images/particles/particle/0.png",
                                                           -1), (25, 25))
            self.rect.x = self.rect.x + 5 if not self.is_left else self.rect.x - 5
            self.slide_count += 1
        if self.slide_count >= 50:
            self.slide_count = 0
            self.is_slide = False
            for i in self.particle_sprite_group:
                i.kill()
            [Particle(self.particle_sprite_group, (self.rect.x, self.rect.y), False, self.screen) for i in range(20)]

    def do_horizontal_and_static_move(self, key):
        if key[pygame.K_d]:
            self.is_left = False
            if not self.is_jumping and not self.is_dash:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 4, self.is_left)
            self.dx += 2

        elif key[pygame.K_a]:
            self.is_left = True
            if not self.is_jumping and not self.is_dash:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 4, self.is_left)
            self.dx -= 2

        else:
            if not self.is_jumping and not self.is_dash:
                if not self.is_jumping:
                    self.image = entities_animations("images/entities/player/idle/{}.png", "idle",
                                                     21, (14, 18), 4,
                                                     self.is_left)

    def do_dash(self):
        if self.dash_count == 50:
            self.dash_count = 0
            self.is_dash = False
        if not self.is_jumping:
            self.image = entities_animations("images/entities/player/slide/{}.png", "slide",
                                             1, (14, 18), 3, self.is_left)
        self.rect.x = self.rect.x + 4 if not self.is_left else self.rect.x - 4
        self.dash_count += 1

    # Функция для отработки движения персонажа
    def do_rotate(self, event):
        key = pygame.key.get_pressed()
        self.dx, self.dy = 0, 0

        if event is not None and event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or key[pygame.K_SPACE]):
                self.is_jumping = True
                self.jumps = self.jumps - 1 if self.jumps > 0 else 2
                self.vel_y = -20 if self.jumps > 0 else self.vel_y
                self.image = entities_animations("images/entities/player/jump/{}.png",
                                                 "jump", 1, (14, 18), 4, self.is_left)

            if event.key == pygame.K_LSHIFT:
                self.image = pygame.transform.scale(load_image("images/particles/particle/0.png",
                                                               -1), (25, 25))
                self.is_slide = True

        # Физика прыжка

        self.vel_y += self.gravity
        if self.vel_y > 20:
            self.vel_y = 20
        self.dy += self.vel_y

        # Физика дэша
        if self.is_dash:
            self.do_dash()

        # Физика и анимация движения по горизонтали и статического положения
        self.do_horizontal_and_static_move(key)

        # Физика слайда
        self.do_slide()
        if self.is_slide:
            return

        if self.particle_sprite_group:  # Если есть спрайты в спрайт-группе
            self.particle_sprite_group.update()
            self.particle_sprite_group.draw(self.screen)

        for tile in self.tile_sprites:

            if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.rect.bottom < tile.rect.centery:
                    self.rect.bottom = tile.rect.top
                    self.dy = 0
                    self.vel_y = 0
                    self.is_jumping = False
                elif self.rect.top > tile.rect.centery:
                    self.rect.top = tile.rect.bottom
            if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                self.dx = 0

        self.rect.x += self.dx
        self.rect.y += self.dy

    def update(self, event=None):
        self.do_rotate(event)
from animations import entities_animations

from image_loader import load_image

from outsiders_objects import Particle

import time

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
        self.gravity = 0.2
        self.dx, self.dy = 0, 0
        # --- Для дэша персонажа
        self.is_dash = False
        self.dash_count = 0
        # --- Для слайда по стене
        self.is_wall_slide = False
        # --- Инициализация картинки, объявления хитбокса и положения относительно экрана
        self.image = pygame.transform.scale(load_image("images/entities/player/idle/0.png", -1),
                                            (self.hero_sizes[0] * 3.5, self.hero_sizes[1] * 3.5))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, 500
        self.rect.width //= 1.5
        self.old_rect = (self.rect.width, self.rect.height)

    # Физика и анимация слайда
    def do_slide(self):
        if self.is_slide:
            self.image = pygame.transform.scale(load_image("images/particles/particle/0.png",
                                                           -1), (25, 25))
            self.check_collide(2.5)
            self.rect.x = self.rect.x + self.dx * 2.5 if not self.is_left else self.rect.x + self.dx * 2.5
            self.slide_count += 1
        if self.slide_count >= 50:
            self.slide_count = 0
            self.is_slide = False
            self.rect.size = self.old_rect
            for i in self.particle_sprite_group:
                i.kill()
            [Particle(self.particle_sprite_group, (self.rect.x, self.rect.y), False, self.screen) for i in range(20)]

    def do_horizontal_and_static_move(self, key):
        if key[pygame.K_d]:
            self.is_left = False
            if not self.is_jumping and not self.is_dash:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 3.5, self.is_left)
            self.dx += 2

        elif key[pygame.K_a]:
            self.is_left = True
            if not self.is_jumping and not self.is_dash:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 3.5, self.is_left)
            self.dx -= 2

        else:
            if not self.is_jumping and not self.is_dash:
                if not self.is_jumping:
                    self.image = entities_animations("images/entities/player/idle/{}.png", "idle",
                                                     21, (14, 18), 3.5,
                                                     self.is_left)

    def do_dash(self):
        if self.dash_count == 50:
            self.dash_count = 0
            self.is_dash = False
        if not self.is_jumping:
            self.image = entities_animations("images/entities/player/slide/{}.png", "slide",
                                             1, (14, 18), 3, self.is_left)
        self.check_collide(2)
        self.rect.x = self.rect.x + self.dx * 2 if not self.is_left else self.rect.x + self.dx * 2
        self.dash_count += 1

    # Функция для отработки движения персонажа
    def do_rotate(self, event):
        self.dx, self.dy = 0, 0
        if event is not None and event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or pygame.key.get_pressed()[pygame.K_SPACE]):
                self.is_jumping = True
                self.gravity = 0.2
                self.jumps = self.jumps - 1 if self.jumps > 0 else 2
                self.vel_y = -7 if self.jumps > 0 else self.vel_y
                self.image = entities_animations("images/entities/player/jump/{}.png",
                                                 "jump", 1, (14, 18), 3.5, self.is_left)
                sound_jump = pygame.mixer.Sound('data/sfx/jump.wav')
                sound_jump.set_volume(0.3)
                sound_jump.play()

            if event.key == pygame.K_LSHIFT:
                self.image = pygame.transform.scale(load_image("images/particles/particle/0.png",
                                                               -1), (25, 25))
                self.is_slide = True
                self.change_rect((self.rect.x, self.rect.y + self.rect.width // 2))
                self.check_collide()
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.is_dash = True
                sound_dash = pygame.mixer.Sound('data/sfx/dash.wav')
                sound_dash.set_volume(0.2)
                sound_dash.play()

        # Физика и анимация движения по горизонтали и статического положения
        self.vel_y += self.gravity
        if self.vel_y > 7:
            self.vel_y = 7
            self.is_jumping = False
        self.dy += self.vel_y

        # Физика прыжка
        self.do_horizontal_and_static_move(pygame.key.get_pressed())

        # Физика дэша
        if self.is_dash and not self.is_jumping:
            self.do_dash()

        # Физика слайда
        self.do_slide()
        if self.is_slide:
            return

        if self.particle_sprite_group:  # Если есть спрайты в спрайт-группе
            self.particle_sprite_group.update()
            self.particle_sprite_group.draw(self.screen)

        self.check_collide()
        self.rect.x += self.dx
        self.rect.y += self.dy

    def check_collide(self, coof=1):
        for tile in self.tile_sprites:
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.rect.bottom < tile.rect.centery:
                    self.rect.bottom = tile.rect.top
                    self.dy = 0
                    self.vel_y = 0
                    self.is_jumping = False
                elif self.rect.top > tile.rect.centery:
                    self.rect.top = tile.rect.bottom
            if tile.rect.colliderect(self.rect.x + self.dx * coof, self.rect.y, self.rect.width, self.rect.height):
                self.rect.size = self.old_rect
                self.dx = 0
                self.is_dash = False
                self.is_slide = False
                if not self.is_jumping:
                    self.image = entities_animations("images/entities/player/wall_slide/{}.png", "wall_slide",
                                                    1, (14, 18), 3, self.is_left)
            if tile.rect.colliderect(self.rect):
                if self.rect.right < tile.rect.centerx:
                    self.rect.right = tile.rect.left
                elif self.rect.left > tile.rect.centerx:
                    self.rect.left = tile.rect.right
                if self.rect.bottom < tile.rect.centery:
                    self.rect.bottom = tile.rect.top
                    self.dy = 0
                    self.vel_y = 0
                    self.is_jumping = False
                elif self.rect.top > tile.rect.centery:
                    self.rect.top = tile.rect.bottom


    def change_rect(self, pos=(0, 0), change_height=0):
        pos = pos if pos[0] != 0 and pos[1] != 0 else (self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        if change_height:
            self.rect.height = change_height
        self.rect.x, self.rect.y = pos

    def update(self, event=None):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)
        self.do_rotate(event)

from animations import entities_animations, dash_animation, EnemyDeath

from image_loader import load_image

from outsiders_objects import Particle

import pygame

import random


class Hero(pygame.sprite.Sprite):
    def __init__(self, screen, sprite, all_sprites, tile_sprites, pos):
        super().__init__(sprite, all_sprites)
        # ---
        self.tile_sprites = tile_sprites
        self.particle_sprite_group = pygame.sprite.Group()
        self.screen = screen
        self.hero_sizes = (14, 18)
        self.is_left = False
        self.hero_death = None
        self.is_hero_death = False
        # --- Взаимодействие с врагом
        self.enemy_sprite = None
        self.enemy_lst = []
        self.new_enemy_dict = {}
        # --- Все для слайда
        self.is_slide = False
        self.is_over = False
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
        # --- Настройка прямоугольгтка игрока
        self.rect = self.image.get_rect()
        self.rect.width //= 1.5
        self.rect.x, self.rect.y = pos
        self.old_rect = (self.rect.width, self.rect.height)
        # ---

    # Физика и анимация слайда
    def do_slide(self):
        '''Функция, отвечающаяя за слайд'''
        if self.is_slide:  # Если переменная is_slide is True, то выполняется слайд
            self.image = dash_animation("images/particles/particle/{}.png", "slide", 3, (12, 12), 3.5)
            self.enemy_collide()
            self.change_rect()
            self.rect.y -= 1
            self.check_collide(coof=3)
            self.rect.x = self.rect.x + self.dx * 3 if not self.is_left else self.rect.x + self.dx * 3
            self.slide_count += 1
        if self.slide_count >= 70:  # Если переменная slide_count >= 70, то слайд заканчивается
            self.kill_and_create_particles_sprites()
            self.is_over = False
            self.slide_count = 0
            self.is_slide = False
            self.rect.size = self.old_rect

    def do_horizontal_and_static_move(self, key):
        '''Функция, отвечающаяя за горизонтальное и статическое положение игрока'''
        if key[pygame.K_d]:
            self.is_left = False
            if not self.is_jumping and not self.is_dash:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 3.5, self.is_left)
            elif self.is_jumping:
                self.image = entities_animations("images/entities/player/jump/{}.png",
                                                 "jump", 1, (14, 18), 3.5, self.is_left)
            self.dx += 2

        elif key[pygame.K_a]:
            self.is_left = True
            if not self.is_jumping and not self.is_dash:
                self.image = entities_animations("images/entities/player/run/{}.png",
                                                 "run", 7, (14, 18), 3.5, self.is_left)
            elif self.is_jumping:
                self.image = entities_animations("images/entities/player/jump/{}.png",
                                                 "jump", 1, (14, 18), 3.5, self.is_left)
            self.dx -= 2
        else:
            if not self.is_jumping and not self.is_dash:
                if not self.is_jumping:
                    self.image = entities_animations("images/entities/player/idle/{}.png", "idle",
                                                     21, (14, 18), 3.5,
                                                     self.is_left)

    def do_dash(self):
        '''Функция, отвечающаяя за дэш'''
        if not self.is_jumping:
            self.image = entities_animations("images/entities/player/slide/{}.png", "slide",
                                             1, (14, 18), 3, self.is_left)
        self.change_rect()
        self.rect.y -= 1
        self.check_collide(coof=2)
        self.rect.x = self.rect.x + self.dx * 2 if not self.is_left else self.rect.x + self.dx * 2
        self.dash_count += 1
        if self.dash_count == 50:
            self.dash_count = 0
            self.is_dash = False
            self.rect.size = self.old_rect

    def kill_and_create_particles_sprites(self):
        '''Функция, отвечающаяя за создание и удаление объектов Particles'''
        for i in self.particle_sprite_group:
            i.kill()
        [Particle(self.particle_sprite_group, (self.rect.x, self.rect.y), False, self.screen,
                  tuple(random.choice(list(range(1, 4)) +
                                      list(range(-3, 0))) for i in range(2))) for i in range(20)]

    def kill_enemies(self):
        for enemy in self.enemy_lst:
            if enemy not in self.new_enemy_dict.keys():
                self.new_enemy_dict[enemy] = EnemyDeath("images/entities/enemy/death/{}.png",
                                                        20, (14, 18), 3.5, 4)
            self.enemy_lst.remove(enemy)
        for enemy, animation in self.new_enemy_dict.copy().items():
            enemy.image = animation.get_image()
            animation.update_animation()
            if animation.index_of_enemy_pic == animation.count_of_files - 1:
                enemy.gun.kill()
                enemy.kill()
                self.new_enemy_dict.pop(enemy)

    def keys_down_up_move(self, event):
        if event is not None and event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_w or pygame.key.get_pressed()[pygame.K_SPACE]) and self.jumps:
                self.check_collide()
                self.is_jumping = True
                self.gravity = 0.2
                self.vel_y = -7 if self.jumps > 0 else self.vel_y
                self.jumps -= 1

                self.image = entities_animations("images/entities/player/jump/{}.png",
                                                 "jump", 1, (14, 18), 3.5, self.is_left)
                sound_jump = pygame.mixer.Sound('data/sfx/jump.wav')
                sound_jump.set_volume(0.3)
                sound_jump.play()

            elif event.key == pygame.K_LSHIFT:
                self.is_over = True
                for i in self.particle_sprite_group:
                    i.kill()
                self.image = pygame.transform.scale(load_image("images/particles/particle/0.png",
                                                               -1), (25, 25))
                self.is_slide = True
                self.check_collide()
                sound_dash = pygame.mixer.Sound('data/sfx/dash.wav')
                sound_dash.set_volume(0.2)
                sound_dash.play()
            elif event.key == pygame.K_LCTRL:
                self.is_dash = True
                if not self.is_jumping:
                    sound_slide = pygame.mixer.Sound('data/sfx/slide.mp3')
                    sound_slide.set_volume(0.2)
                    sound_slide.play()
            elif event is not None and event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.rect.size = self.old_rect
                    self.is_dash = False
                    self.dash_count = 0
                if event.key == pygame.K_LSHIFT:
                    self.is_slide = False
                    self.rect.size = self.old_rect
                    self.slide_count = 0
                    if self.is_over:
                        self.kill_and_create_particles_sprites()

    def enemy_collide(self):
        for enemy in self.enemy_sprite:
            if enemy.rect.colliderect(self.rect):
                if enemy not in self.enemy_lst:
                    self.enemy_lst.append(enemy)
    '''for enemy in self.enemy_lst:
            if enemy not in self.new_enemy_dict.keys():
                self.new_enemy_dict[enemy] = EnemyDeath("images/entities/enemy/death/{}.png",
                                                        20, (14, 18), 3.5)
            self.enemy_lst.remove(enemy)
        for enemy, animation in self.new_enemy_dict.copy().items():
            enemy.image = animation.get_image()
            animation.update_animation()
            if animation.index_of_enemy_pic == animation.count_of_files - 1:
                enemy.gun.kill()
                enemy.kill()
                self.new_enemy_dict.pop(enemy)'''

    def check_collide(self, coof=1):
        for tile in self.tile_sprites:
            for enemy in self.enemy_sprite:
                for projectiles in enemy.list_of_projectiles:
                    if projectiles.rect.colliderect(self.rect):
                        if self.hero_death is None:
                            self.hero_death = EnemyDeath("images/entities/player/death/{}.png", 27, (14, 18), 3.5, 3, self.is_left)
                        self.is_hero_death = True
                    elif (projectiles.rect.colliderect(tile.rect) or projectiles.rect.left
                          >= self.screen.get_width() or projectiles.rect.right <= 0):
                        projectiles.kill()

            if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.rect.top > tile.rect.centery:
                    self.rect.top = tile.rect.bottom
                else:
                    self.rect.bottom = tile.rect.top - 1
                    self.dy = 0
                    self.vel_y = 0
                    self.jumps = 2
                    self.is_jumping = False

            if tile.rect.colliderect(self.rect.x + self.dx * coof, self.rect.y, self.rect.width, self.rect.height):
                self.rect.size = self.old_rect
                self.dx = 0
                self.is_dash = False
                self.is_slide = False
                self.jumps = 2
                self.is_jumping = False
                if self.is_left:
                    self.image = pygame.transform.scale(load_image("images/entities/player/wall_slide/1.png", -1, self.is_left),
                                                        (self.hero_sizes[0] * 3.5, self.hero_sizes[1] * 3.5))
                else:
                    self.image = pygame.transform.scale(load_image("images/entities/player/wall_slide/0.png", -1),
                                                        (self.hero_sizes[0] * 3.5, self.hero_sizes[1] * 3.5))

            if tile.rect.colliderect(self.rect):
                if self.rect.right < tile.rect.centerx:
                    self.rect.right = tile.rect.left
                elif self.rect.left > tile.rect.centerx:
                    self.rect.left = tile.rect.right
                if self.rect.top >= tile.rect.centery:
                    self.rect.top = tile.rect.bottom
                else:
                    self.rect.bottom = tile.rect.top
                    self.jumps = 2
                    self.dy = 0
                    self.vel_y = 0
                    self.is_jumping = False

    def change_rect(self, pos=(0, 0), change_height=0):
        pos = pos if pos[0] != 0 and pos[1] != 0 else (self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        if change_height:
            self.rect.height = change_height
        self.rect.x, self.rect.y = pos

    def player_rotate(self, event=None):
        '''Функция, отвечающаяя за перемещение игроков по экрану'''
        self.kill_enemies()

        self.dx, self.dy = 0, 0
        self.do_horizontal_and_static_move(pygame.key.get_pressed())

        self.keys_down_up_move(event=event)

        # Физика и анимация движения по горизонтали и статического положения
        self.check_collide()
        self.vel_y += self.gravity
        if self.vel_y > 7:
            self.vel_y = 7
            self.is_jumping = False
        self.dy += self.vel_y

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
        if self.is_hero_death:
            self.image = self.hero_death.get_image()
            self.hero_death.update_animation()
            if self.hero_death.index_of_enemy_pic == self.hero_death.count_of_files - 1:
                self.kill()

        self.rect.x += self.dx
        self.rect.y += self.dy

    def update(self, enemy_sprite, event=None):
        self.enemy_sprite = enemy_sprite
        self.player_rotate(event=event)


class Gun(pygame.sprite.Sprite):
    def __init__(self, guns_sprite_group, all_sprites):
        super().__init__(guns_sprite_group, all_sprites)
        self.image = pygame.transform.scale(load_image("images/gun.png", (0, 0, 0)), (20, 12))
        self.rect = self.image.get_rect()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, projectile_sprite_group, all_spirtes, pos, hero_coordinates):
        super().__init__(projectile_sprite_group, all_spirtes)
        self.image = pygame.transform.scale(load_image("images/projectile.png", (0, 0, 0)), (20, 13))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.shoot_time = 0  # В дальнейгем поставим n секунд
        self.hero_coordinates = hero_coordinates
        self.dx = 5
        self.find_path()

    def find_path(self):
        if self.hero_coordinates[0] - self.rect.x > 0:
            self.dx = 5
        else:
            self.dx = -5

    def update(self):
        self.rect = self.rect.move(self.dx, 0)


class Enemies(pygame.sprite.Sprite):
    def __init__(self, screen, enemies_sprite_group, all_sprite_group, tile_sprite_group, pos, check_coords, gun):
        super().__init__(enemies_sprite_group, all_sprite_group)
        self.gun = gun
        self.hero_spite_group = None
        self.tile_sprite_group = tile_sprite_group
        self.all_sprites = all_sprite_group
        self.list_of_projectiles = []
        self.cooldown = 0
        self.projectile_sprite_group = pygame.sprite.Group()
        self.screen = screen
        self.dx = random.choice([-1, 1])
        self.is_left = False if self.dx > 0 else True
        self.image = EnemyDeath("images/entities/enemy/idle/{}.png",
                                15, (14, 18), 3.5, self.is_left).get_image()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.static = EnemyDeath("images/entities/enemy/idle/{}.png", 16, (14, 18), 3.5, 10)
        self.vel_y = 40
        self.gravity = 0.2
        self.dy, self.dx = 0, 0
        self.rect.width //= 1.4
        self.check_coords = check_coords
        # self.rect.width //= 2
        # self.rect.height //= 1.25

    def check_collison(self):
        for tile in self.tile_sprite_group:
            if tile.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.rect.top > tile.rect.centery:
                    self.rect.top = tile.rect.bottom
                else:
                    self.rect.bottom = tile.rect.top
                    self.dy = 0
                    self.vel_y = 0
            # if not self.check_coords([self.rect.x + self.dx, self.rect.y + self.dy]):
            #     self.dx = -self.dx
            # if tile.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
            #     self.dx = -self.dx

            if tile.rect.colliderect(self.rect):
                # if self.rect.right < tile.rect.centerx:
                #     self.rect.right = tile.rect.left
                # elif self.rect.left > tile.rect.centerx:
                #     self.rect.left = tile.rect.right
                if self.rect.top >= tile.rect.centery:
                    self.rect.top = tile.rect.bottom
                else:
                    self.rect.bottom = tile.rect.top
                    self.dy = 0
                    self.vel_y = 0

    def detect_hero(self):
        for hero in self.hero_spite_group:
            if hero.rect.y in range(self.rect.y - 30, self.rect.y + 31):
                if self.cooldown == 50:
                    self.list_of_projectiles.append(Projectile(self.projectile_sprite_group, self.all_sprites,
                                                               (self.rect.x + self.rect.width // 2 + 2,
                                                                self.rect.y + self.rect.height // 2), (hero.rect.centerx, hero.rect.centery)))
                    self.cooldown = 0
                else:
                    self.cooldown += 1

    def do_enemy_rotate(self):
        # self.vel_y = 40
        self.gun_image = load_image("images/gun.png")
        self.gun.rect.x, self.gun.rect.y = self.rect.x + self.rect.width // 2 + 2, self.rect.y + self.rect.height // 2
        self.dy = 0
        self.check_collison()
        self.vel_y += self.gravity
        if self.vel_y > 7:
            self.vel_y = 7
        self.dy += self.vel_y
        self.image = self.static.get_image()
        self.static.update_animation()
        self.detect_hero()
        self.projectile_sprite_group.draw(self.screen)
        self.projectile_sprite_group.update()
        # self.projectile_sprite_group.update()

        self.rect.y += self.dy
        self.rect.x += self.dx

    def update(self, hero_spite_group):
        self.hero_spite_group = hero_spite_group
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)
        self.do_enemy_rotate()

from image_loader import load_image

import pygame


index, index_of_hero_pic = 0, 0
type_of_move = None
index_particles, index_of_particles_pic = 0, 0

type_of_move_particle = None
index_of_exp, index_of_exp_img = 0, 0

index_of_enemy_death, index_of_enemy_death_pic = 0, 0

index_of_hero_death, index_of_hero_death_pic = 0, 0

index_of_fire_ball, index_of_fire_ball_pic = 0, 0

index_of_hero_for_fire_ball, index_of_hero_for_ball_pic = 0, 0

index_of_slide, index_of_slide_pic = 0, 0

index_of_enemy, index_of_enemy_pic, type_of_enemy_move = 0, 0, None


def enemy_death(path, count_of_files, size, mul_num, is_reversed=False):
    global index_of_enemy_death, index_of_enemy_death_pic
    image = pygame.transform.scale(load_image(path.format(index_of_enemy_death_pic), -1, is_reversed),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index_of_enemy_death == 10:
        index_of_enemy_death_pic += 1
        index_of_enemy_death = 0
    if index_of_enemy_death_pic == count_of_files:
        index_of_enemy_death_pic = 0

    index_of_enemy_death += 1
    return image, index_of_enemy_death_pic


def hero_death(path, count_of_files, size, mul_num, is_reversed=False):
    global index_of_hero_death, index_of_hero_death_pic
    image = pygame.transform.scale(load_image(path.format(index_of_hero_death_pic), -1, is_reversed),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index_of_hero_death == 1:
        index_of_hero_death_pic += 1
        index_of_hero_death = 0
    if index_of_hero_death_pic == count_of_files:
        index_of_hero_death_pic = 0

    index_of_hero_death += 1
    return image


def fire_ball(path, count_of_files, size, mul_num, is_reversed=False):
    global index_of_fire_ball, index_of_fire_ball_pic
    image = pygame.transform.scale(load_image(path.format(index_of_fire_ball_pic), -1, is_reversed),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index_of_fire_ball == 1:
        index_of_fire_ball_pic += 1
        index_of_fire_ball = 0
    if index_of_fire_ball_pic == count_of_files:
        index_of_fire_ball_pic = 0

    index_of_fire_ball += 1
    return image


def hero_for_fire_ball(path, count_of_files, size, mul_num, is_reversed=False):
    global index_of_hero_for_fire_ball, index_of_hero_for_ball_pic
    image = pygame.transform.scale(load_image(path.format(index_of_hero_for_ball_pic), -1, is_reversed),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index_of_hero_for_fire_ball == 1:
        index_of_hero_for_ball_pic += 1
        index_of_hero_for_fire_ball = 0
    if index_of_hero_for_ball_pic == count_of_files:
        index_of_hero_for_ball_pic = 0

    index_of_hero_for_fire_ball += 1
    return image


def entities_animations(path, type_of_ev, count_of_files, size, mul_num, is_reversed=False):
    global index, index_of_hero_pic, type_of_move
    if type_of_ev != type_of_move:
        type_of_move = type_of_ev
        index, index_of_hero_pic = 0, 0
    image = pygame.transform.scale(load_image(path.format(index_of_hero_pic), -1, is_reversed),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index == 10:
        index_of_hero_pic += 1
        index = 0
    if index_of_hero_pic == count_of_files:
        index_of_hero_pic = 0
    index += 1
    return image


def particles_animation(path, type_of_ev, count_of_files, size, mul_num):
    global index_particles, index_of_particles_pic, type_of_move_particle
    image = pygame.transform.scale(load_image(path.format(index_of_particles_pic), -1),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index_particles == 400:
        index_of_particles_pic += 1
        index_particles = 0
    if index_of_particles_pic == count_of_files:
        index_of_particles_pic = 0
    index_particles += 1
    return image


def dash_animation(path, type_of_ev, count_of_files, size, mul_num):
    global index_of_slide, index_of_slide_pic
    image = pygame.transform.scale(load_image(path.format(index_of_slide_pic), -1),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index_of_slide == 10:
        index_of_slide_pic += 1
        index_of_slide = 0
    if index_of_slide_pic == count_of_files:
        index_of_slide_pic = 0
    index_of_slide += 1
    return image


class EnemyDeath:
    def __init__(self, path, count_of_files, size, mul_num, animation_time=6, is_kill=False, is_reversed=False):
        self.path = path
        self.count_of_files = count_of_files
        self.index_of_enemy_pic = 0
        self.index_of_enemy = 0
        self.is_reversed = is_reversed
        self.size = size
        self.mul_num = mul_num
        self.is_kill = is_kill
        self.animation_time = animation_time
        self.image = pygame.transform.scale(load_image(self.path.format(self.index_of_enemy_pic), -1, self.is_reversed),
                                            (self.size[0] * self.mul_num, self.size[1] * self.mul_num))

    def get_image(self):
        return self.image

    def update_animation(self):
        if self.index_of_enemy == self.animation_time:
            self.index_of_enemy_pic += 1
            self.index_of_enemy = 0
        if self.index_of_enemy_pic == self.count_of_files:
            self.index_of_enemy_pic = 0
        self.image = pygame.transform.scale(load_image(self.path.format(self.index_of_enemy_pic), -1, self.is_reversed),
                                            (self.size[0] * self.mul_num, self.size[1] * self.mul_num))
        self.index_of_enemy += 1


class Camera:
    def __init__(self, screen):
        self.dx = 0
        self.dy = 0
        self.screen = screen

    def apply(self, obj):
        obj.rect.x += self.dx // 50
        obj.rect.y += self.dy // 50

    def update(self, target, coof=2):
        self.dx = -(target.rect.x + target.rect.w // coof - self.screen.get_width() // coof)
        self.dy = -(target.rect.y + target.rect.h // coof - self.screen.get_height() // coof)

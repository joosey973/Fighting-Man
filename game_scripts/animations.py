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



def enemy_death(path, count_of_files, size, mul_num, is_reversed=False):
    global index_of_enemy_death, index_of_enemy_death_pic
    image = pygame.transform.scale(load_image(path.format(index_of_enemy_death_pic), -1, is_reversed),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index_of_enemy_death == 1:
        index_of_enemy_death_pic += 1
        index_of_enemy_death = 0 
    if index_of_enemy_death_pic == count_of_files:
        index_of_enemy_death_pic = 0
    
    index_of_enemy_death += 1
    return image


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
    if index == 3:
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


def exploison_animation(path, count_of_files, ex):
    global index_of_exp, index_of_exp_img
    image = pygame.transform.scale(load_image(path.format(index_of_exp_img), -1), (80, 80))
    if index_of_exp == 1:
        index_of_exp_img += 1
        index_of_exp = 0
    if index_of_exp_img == count_of_files:
        ex.istrue = False
    index_of_exp += 1
    return image, index_of_exp_img


class Camera:
    def __init__(self, screen):
        self.dx = 0
        self.dy = 0
        self.screen = screen

    def apply(self, obj):
        obj.rect.x += self.dx // 10
        obj.rect.y += self.dy // 10

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.screen.get_width() // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.screen.get_height() // 2)

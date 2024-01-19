from image_loader import load_image

import pygame


index, index_of_hero_img = 0, 0
type_of_move = None
index_particles, index_of_particles_img = 0, 0
type_of_move_particle = None
index_of_exp, index_of_exp_img = 0, 0


def entities_animations(path, type_of_ev, count_of_files, size, mul_num, is_reversed=False):
    global index, index_of_hero_img, type_of_move
    if type_of_ev != type_of_move:
        type_of_move = type_of_ev
        index, index_of_hero_img = 0, 0
    image = pygame.transform.scale(load_image(path.format(index_of_hero_img), -1, is_reversed),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index == 10:
        index_of_hero_img += 1
        index = 0
    if index_of_hero_img == count_of_files:
        index_of_hero_img = 0
    index += 1
    return image


def particles_animation(path, type_of_ev, count_of_files, size, mul_num):
    global index_particles, index_of_particles_img, type_of_move_particle
    image = pygame.transform.scale(load_image(path.format(index_of_particles_img), -1),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index_particles == 400:
        index_of_particles_img += 1
        index_particles = 0
    if index_of_particles_img == count_of_files:
        index_of_particles_img = 0
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

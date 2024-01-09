from image_loader import load_image

import pygame


index, index_of_hero_pos = 0, 0
type_of_move = None
index_particles, index_of_particles_pos = 0, 0
type_of_move_particle = None


def entities_animations(path, type_of_ev, count_of_files, size, mul_num, is_reversed=False):
    global index, index_of_hero_pos, type_of_move
    if type_of_ev != type_of_move:
        type_of_move = type_of_ev
        index, index_of_hero_pos = 0, 0
    image = pygame.transform.scale(load_image(path.format(index_of_hero_pos), -1, is_reversed),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index == 3:
        index_of_hero_pos += 1
        index = 0
    if index_of_hero_pos == count_of_files:
        index_of_hero_pos = 0
    index += 1
    return image


def particles_animation(path, type_of_ev, count_of_files, size, mul_num):
    global index_particles, index_of_particles_pos, type_of_move_particle
    image = pygame.transform.scale(load_image(path.format(index_of_particles_pos), -1),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index_particles == 500:
        index_of_particles_pos += 1
        index_particles = 0
    if index_of_particles_pos == count_of_files:
        index_of_particles_pos = 0
    index_particles += 1
    return image


class Camera:
    def __init__(self, screen):
        self.dx = 0
        self.dy = 0
        self.screen = screen

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.screen.get_width() // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.screen.get_height() // 2)

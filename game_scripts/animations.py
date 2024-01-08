from image_loader import load_image

import pygame


index, index_of_hero_pos = 0, 0
type_of_move = None
index_particles, index_of_particles_pos = 0, 0
type_of_move_particle = None


def entities_animations(path, type_of_ev, count_of_files, size, mul_num, is_reversed):
    global index, index_of_hero_pos, type_of_move
    if type_of_ev != type_of_move:
        type_of_move = type_of_ev
        index, index_of_hero_pos = 0, 0
    image = pygame.transform.scale(load_image(path.format(index_of_hero_pos), -1, is_reversed),
                                   (size[0] * mul_num, size[1] * mul_num))
    if index == 5:
        index_of_hero_pos += 1
        index = 0
    if index_of_hero_pos == count_of_files:
        index_of_hero_pos = 0
    index += 1
    return image

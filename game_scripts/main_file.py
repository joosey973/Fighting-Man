import random
import sys

from CharactersPhysics import Hero

from collide_system import Boarders

from image_loader import load_image

from outsiders_objects import Clouds, Particles

import pygame


class Game:
    def __init__(self):
        self.width, self.height = 1000, 1000
        self.start_len_of_particles = 150
        self.start_len_of_clouds = (self.width * self.height // 100000) + 5
        self.particles_var = ["leaf", "particle"]
        self.create_groups()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = pygame.time.Clock()
        self.activate_sprites()

    def create_groups(self):
        self.hero_sprite = pygame.sprite.Group()
        self.vertical_borders = pygame.sprite.Group()
        self.horizontal_borders = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.clouds_sprites = pygame.sprite.Group()

    def activate_sprites(self):
        Boarders(5, 5, self.screen.get_width() - 5, 5, self.vertical_borders, self.horizontal_borders,
                 self.all_sprites)
        Boarders(5, self.screen.get_height() - 5, self.screen.get_width() - 5, self.screen.get_height() - 5,
                 self.vertical_borders, self.horizontal_borders, self.all_sprites)
        Boarders(5, 5, 5, self.screen.get_height() - 5, self.vertical_borders,
                 self.horizontal_borders, self.all_sprites)
        Boarders(self.screen.get_width() - 5, 5, self.screen.get_width() - 5, self.screen.get_height() - 5,
                 self.vertical_borders, self.horizontal_borders, self.all_sprites)
        [Particles(self.screen, self.particles_var[random.randrange(2)], self.particles,
                   self.horizontal_borders, self.all_sprites)
         for _ in range(self.start_len_of_particles)]
        Hero(self.screen, self.hero_sprite)
        [Clouds(self.screen, random.randrange(1, 3), self.clouds_sprites, self.vertical_borders)
         for _ in range(self.start_len_of_clouds)]

    def update_sprites(self, key):
        self.clouds_sprites.update()
        self.clouds_sprites.draw(self.screen)

        self.particles.update()
        self.particles.draw(self.screen)

        self.hero_sprite.update(key)
        self.hero_sprite.draw(self.screen)

    def run(self):
        is_running = True
        key = pygame.key.get_pressed()
        while is_running:
            for _ in range((self.start_len_of_particles - len(self.particles)) * 2):
                Particles(self.screen, self.particles_var[random.randrange(2)],
                          self.particles, self.horizontal_borders, self.all_sprites)
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                key = pygame.key.get_pressed()
            self.update_sprites(key)
            self.fps.tick(25)
            pygame.display.update()


if __name__ == "__main__":
    Game().run()

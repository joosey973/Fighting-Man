import random
import sys

from CharactersPhysics import Hero

from collide_system import Boarders

from image_loader import load_image

from particles_movement import Particles

import pygame


class Game:
    def __init__(self):
        self.width, self.height = 600, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = pygame.time.Clock()
        self.hero_sprite = pygame.sprite.Group()
        self.vertical_borders = pygame.sprite.Group()
        self.horizontal_borders = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.particles_var = ["leaf", "particle"]
        self.activate_sprites()

    def activate_sprites(self):
        Hero(self.screen, self.hero_sprite, self.all_sprites)
        Boarders(5, 5, self.screen.get_width() - 5, 5, self.vertical_borders, self.horizontal_borders, self.all_sprites)
        Boarders(5, self.screen.get_height() - 5, self.screen.get_width() - 5, self.screen.get_height() - 5,
                 self.vertical_borders, self.horizontal_borders, self.all_sprites)
        Boarders(5, 5, 5, self.screen.get_height() - 5, self.vertical_borders,
                 self.horizontal_borders, self.all_sprites)
        Boarders(self.screen.get_width() - 5, 5, self.screen.get_width() - 5, self.screen.get_height() - 5,
                 self.vertical_borders, self.horizontal_borders, self.all_sprites)
        [Particles(self.screen, self.particles_var[random.randrange(2)], self.particles) for _ in range(50)]
        Hero(self.hero_sprite)

    def run(self):
        is_running = True
        key = pygame.key.get_pressed()
        while is_running:
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                key = pygame.key.get_pressed()
            self.hero_sprite.update(key)
            self.hero_sprite.draw(self.screen)
            self.particles.update()
            self.particles.draw(self.screen)
            self.fps.tick(100)
            pygame.display.update()


if __name__ == "__main__":
    Game().run()

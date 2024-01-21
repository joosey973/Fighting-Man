import sys

from CharactersPhysics import Hero

from animations import Camera, enemy_death, hero_death

from collide_system import Boarders

from image_loader import load_image

from outsiders_objects import Clouds, Particles

import pygame


class Game:
    def __init__(self):
        self.width, self.height = 1000, 1000
        self.start_len_of_particles = 25
        self.start_len_of_clouds = (self.width * self.height // 100000) + 5
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
        [Particles(self.screen, "leaf", self.particles, self.horizontal_borders, self.vertical_borders,
                   self.all_sprites) for _ in range(self.start_len_of_particles)]
        [Clouds(self.screen, self.clouds_sprites, self.all_sprites) for _ in range(self.start_len_of_clouds)]

    def update_sprites(self):
        self.clouds_sprites.update()  # Апдейт облаков
        self.clouds_sprites.draw(self.screen)

        self.particles.update()  # Апдейт листьев
        self.particles.draw(self.screen)

        self.hero_sprite.update()  # Апдейт главного героя
        self.hero_sprite.draw(self.screen)

    def run(self):
        is_running = True
        hero = Hero(self.screen, self.hero_sprite, self.all_sprites)
        camera = Camera(self.screen)
        while is_running:
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))
            [Particles(self.screen, "leaf", self.particles, self.horizontal_borders, self.vertical_borders,
                       self.all_sprites) for _ in range(self.start_len_of_particles - len(self.particles))]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.fps.tick(20)
            camera.update(hero)
            for sprite in self.all_sprites:
                camera.apply(sprite)
            self.update_sprites()
            self.screen.blit(enemy_death('images/entities/enemy/death/{}.png', 21, (14, 18), 10), (200, 700))
            self.screen.blit(enemy_death('images/entities/enemy/death1/{}.png', 21, (14, 18), 10), (200, 200))
            self.screen.blit(hero_death('images/entities/player/death/{}.png', 27, (14, 18), 3), (400, 400))

            pygame.display.update()


if __name__ == "__main__":
    Game().run()

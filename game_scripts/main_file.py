import sys

from CharactersPhysics import Hero

from animations import Camera, enemy_death, hero_death, fire_ball, hero_for_fire_ball

from collide_system import Boarders

from image_loader import load_image

from outsiders_objects import Clouds, Particles

from tilemap import Tilemap

import json

from menu import Menu

import pygame


class Game:
    def __init__(self):
        self.width, self.height = 960, 600
        self.start_len_of_particles = 25
        self.start_len_of_clouds = (self.width * self.height // 100000) + 5
        self.create_groups()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.hero = Hero(self.screen, self.hero_sprite, self.all_sprites, self.tilemap_sprites)
        self.fps = pygame.time.Clock()
        self.clouds_speed = pygame.USEREVENT + 1
        pygame.time.set_timer(self.clouds_speed, 300)
        self.leafs_speed = pygame.USEREVENT + 2
        pygame.time.set_timer(self.leafs_speed, 60)
        self.tilemap = self.generate_map()
        self.activate_sprites()
        self.button = Menu(self.width / 2 - (200 / 2), 300, 200, 90, 'Старт', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')

    def render_map(self):
        for objects_decor in self.tilemap['offgrid']:
            coord = "offgrid"
            Tilemap(coord, objects_decor['pos'], objects_decor['type'], objects_decor['variant'], self.tilemap_sprites,
                    self.other_sprite_group, self.all_sprites)
        for objects in self.tilemap["tilemap"]:
            value_object = self.tilemap['tilemap'][objects]
            coord = 'tilemap'
            Tilemap(coord, value_object['pos'], value_object['type'], value_object["variant"], self.tilemap_sprites,
                    self.other_sprite_group, self.all_sprites)

    def generate_map(self):
        with open('levels/level_1.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def create_groups(self):
        self.hero_sprite = pygame.sprite.Group()
        self.vertical_borders = pygame.sprite.Group()
        self.horizontal_borders = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.clouds_sprites = pygame.sprite.Group()
        self.tilemap_sprites = pygame.sprite.Group()
        self.other_sprite_group = pygame.sprite.Group()

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
        self.render_map()

    def update_sprites(self):
        self.clouds_sprites.update()  # Апдейт облаков
        self.clouds_sprites.draw(self.screen)

        self.particles.update()  # Апдейт листьев
        self.particles.draw(self.screen)

        self.other_sprite_group.draw(self.screen)
        self.tilemap_sprites.draw(self.screen)

        self.hero_sprite.update()  # Апдейт главного героя
        self.hero_sprite.draw(self.screen)
    
    def menu(self):
        menu = True
        while menu:
            self.screen.fill((0, 0, 0))
            self.button.check_hover(pygame.mouse.get_pos())
            self.button.draw(self.screen)
            self.fps.tick(80)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and event.button == self.button:
                    self.run()
                self.button.handle_event(event)

    def run(self):
        pygame.mixer.init()
        pygame.mixer.music.load('data/music_minecraft.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        pygame.mouse.set_visible(False)
        is_running = True
        camera = Camera(self.screen)
        count = 0
        coof = 100
        camera.update(self.hero, coof)
        for sprite in self.all_sprites:
            camera.apply(sprite)
        while is_running:
            if count < 30:
                count += 1
            else:
                coof = 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.clouds_speed:
                    self.clouds_sprites.update(True)
                if event.type == self.leafs_speed:
                    self.particles.update(True)
                self.hero.update(event)
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))
            [Particles(self.screen, "leaf", self.particles, self.horizontal_borders, self.vertical_borders,
                       self.all_sprites) for _ in range(self.start_len_of_particles - len(self.particles))]
            camera.update(self.hero, coof)
            for sprite in self.all_sprites:
                camera.apply(sprite)
            self.update_sprites()
            self.fps.tick(80)
            pygame.display.update()


if __name__ == "__main__":
    Game().menu()

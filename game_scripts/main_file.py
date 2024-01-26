import sys

from CharactersPhysics import Hero, Enemies

from animations import Camera

from collide_system import Boarders

from image_loader import load_image

from outsiders_objects import Clouds, Particles

from tilemap import Tilemap

import json

from menu import Menu

import pygame


class Game:
    def __init__(self):
        self.sound()
        self.width, self.height = 800, 600
        self.start_len_of_particles = 25
        self.start_len_of_clouds = (self.width * self.height // 100000) + 5
        self.create_groups()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.hero = None
        self.enemy = None
        self.fps = pygame.time.Clock()
        self.clouds_speed = pygame.USEREVENT + 1
        pygame.time.set_timer(self.clouds_speed, 100)
        self.leafs_speed = pygame.USEREVENT + 2
        pygame.time.set_timer(self.leafs_speed, 60)
        self.tilemap = self.generate_map()
        self.activate_sprites()

        

    def sound(self, volume=0.1):
        pygame.mixer.init()
        pygame.mixer.music.load('data/music_minecraft.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)

    def render_map(self):
        for objects_decor in self.tilemap['offgrid']:
            coord = "offgrid"
            tile = Tilemap(coord, objects_decor['pos'], objects_decor['type'], objects_decor['variant'],
                           self.tilemap_sprites, self.other_sprite_group, self.all_sprites)
            if objects_decor['type'] == "player":
                self.hero = Hero(self.screen, self.hero_sprite, self.all_sprites, self.tilemap_sprites, tile.get_pos())
                tile.kill()
                continue
            if objects_decor['type'] == "enemy":
                Enemies(self.screen, self.enemies_sprite_group, self.all_sprites, self.tilemap_sprites, tile.get_pos())
                tile.kill()
                continue

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
        self.enemies_sprite_group = pygame.sprite.Group()

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
        self.render_map()

    def update_sprites(self):
        self.clouds_sprites.update()  # Апдейт облаков
        self.clouds_sprites.draw(self.screen)

        self.particles.update()  # Апдейт листьев
        self.particles.draw(self.screen)

        self.other_sprite_group.draw(self.screen)
        self.tilemap_sprites.draw(self.screen)

        self.hero_sprite.update(self.enemies_sprite_group)  # Апдейт главного героя
        self.hero_sprite.draw(self.screen)

        self.enemies_sprite_group.draw(self.screen)
        self.enemies_sprite_group.update()

    def menu(self):
        self.start_button = Menu(self.width / 2 - (200 / 2), self.height - 570, 200, 90, 'Старт', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        self.settings_button = Menu(self.width / 2 - (200 / 2), self.height - 470, 200, 90, 'Настройки', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        self.exit_button = Menu(self.width / 2 - (200 / 2), self.height - 370, 200, 90, 'Выйти', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        pygame.mouse.set_visible(True)
        menu = True
        [Clouds(self.screen, self.clouds_sprites, self.all_sprites) for _ in range(self.start_len_of_clouds)]
        while menu:
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))

            self.start_button.check_hover(pygame.mouse.get_pos())
            self.start_button.draw(self.screen)
            self.settings_button.check_hover(pygame.mouse.get_pos())
            self.settings_button.draw(self.screen)
            self.exit_button.check_hover(pygame.mouse.get_pos())
            self.exit_button.draw(self.screen)
            self.fps.tick(80)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and event.button == self.start_button:
                    menu = False
                    self.run()
                if event.type == pygame.USEREVENT and event.button == self.settings_button:
                    menu = False
                    self.settings()
                if event.type == pygame.USEREVENT and event.button == self.exit_button:
                    menu = False
                    pygame.quit()
                    sys.exit()
                for btn in [self.start_button, self.settings_button, self.exit_button]:
                    btn.indent(self.width / 2 - (200 / 2))
                self.start_button.handle_event(event)
                self.settings_button.handle_event(event)
                self.exit_button.handle_event(event)

    def settings(self):
        audio_button = Menu(self.width / 2 - (200 / 2), self.height - 570, 200, 90, 'Аудио', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        video_button = Menu(self.width / 2 - (200 / 2), self.height - 470, 200, 90, 'Видео', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        back_button = Menu(self.width / 2 - (200 / 2), self.height - 370, 200, 90, 'Назад', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        running = True
        while running:
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))
            font = pygame.font.Font(None, 56)
            text_surface = font.render('', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width / 2, 100))
            self.screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.menu()
                    running = False
                if event.type == pygame.USEREVENT and event.button == video_button:
                    self.video_settings()
                    running = False
                    for btn in [audio_button, video_button, back_button]:
                        btn.indent(self.width / 2 - (200 / 2))
                if event.type == pygame.USEREVENT and event.button == audio_button:
                    self.audio_settings()
                    running = False
                for btn in [audio_button, video_button, back_button]:
                    btn.handle_event(event)
            for btn in [audio_button, video_button, back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.screen)

            pygame.display.update()

    def video_settings(self):
        video_mode_1_button = Menu(self.width / 2 - (200 / 2), self.height - 570, 200, 90, '800x600', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        video_mode_2_button = Menu(self.width / 2 - (200 / 2), self.height - 470, 200, 90, '1280x1024', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        video_mode_3_button = Menu(self.width / 2 - (200 / 2), self.height - 370, 200, 90, 'Full HD', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        back_button = Menu(self.width / 2 - (200 / 2), self.height - 270, 200, 90, 'Назад', 'data/images/buttons/start.png', 'data/images/buttons/start_hover.png', 'data/sfx/button.mp3')
        running = True
        while running:
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))
            font = pygame.font.Font(None, 56)
            text_surface = font.render('', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width / 2, 100))
            self.screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.settings()
                    running = False
                if event.type == pygame.USEREVENT and event.button == video_mode_1_button:
                    self.video_mode_update(800, 600)
                    self.settings()
                if event.type == pygame.USEREVENT and event.button == video_mode_2_button:
                    self.video_mode_update(1280, 1024)
                    self.settings()
                if event.type == pygame.USEREVENT and event.button == video_mode_3_button:
                    self.video_mode_update(1920, 1080, pygame.FULLSCREEN)
                    self.settings()
                for btn in [video_mode_1_button, video_mode_2_button, video_mode_3_button, back_button]:
                    btn.handle_event(event)
            for btn in [video_mode_1_button, video_mode_2_button, video_mode_3_button, back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.screen)
            
            pygame.display.update()

    def video_mode_update(self, width, height, fullsc=0):
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height), fullsc)
        self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (width, height)), (0, 0))

    def audio_settings(self):
        print('zxc')

    def run(self):
        pygame.mouse.set_visible(False)
        is_running = True
        camera = Camera(self.screen)
        count = 0
        coof = 100
        camera.update(self.hero, coof)
        for sprite in self.all_sprites:
            camera.apply(sprite)
        pygame.time.set_timer(self.clouds_speed, 300)
        [Clouds(self.screen, self.clouds_sprites, self.all_sprites) for _ in range(self.start_len_of_clouds)]
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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()
                        is_running = False
                self.hero.update(event)
                self.hero.update(self.enemies_sprite_group, event=event)

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

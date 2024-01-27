import sys

from CharactersPhysics import Hero, Enemies, Gun

from animations import Camera

from image_loader import load_image

from outsiders_objects import Clouds, Particles

from tilemap import Tilemap

from save_info import get_info, insert_info

import json

from menu import Menu

import pygame

import os


class Game:
    def __init__(self):
        if not os.path.isfile("files/info.db"):
            insert_info()
        self.sound()
        self.width, self.height = list(map(int, get_info('''select Resolution from game_info''').split(", ")))
        self.count_of_map = get_info('''select Level from game_info''')
        self.start_len_of_particles = 25
        self.transition = -50
        self.minimun = 0
        self.start_len_of_clouds = (self.width * self.height // 100000) + 5
        self.create_groups()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.hero = None
        self.enemy = None
        self.fps = pygame.time.Clock()
        self.clouds_speed = pygame.USEREVENT + 1
        self.leafs_speed = pygame.USEREVENT + 2
        pygame.time.set_timer(self.leafs_speed, 60)
        self.tilemap = self.generate_map(self.count_of_map)
        self.activate_sprites()
        self.new_mouse = pygame.image.load('data/images/arrow/arrow.png')

    def check_coord(self, pos):
        for objects in self.tilemap["tilemap"]:
            value_object = self.tilemap["tilemap"][objects]
            if value_object['pos'] == pos:
                return True
            else:
                return False

    def sound(self, volume=0.0):
        pygame.mixer.init()
        pygame.mixer.music.load('data/music_minecraft.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)

    def render_map(self):
        for objects_decor in self.tilemap['offgrid']:
            coord = "offgrid"
            tile = Tilemap(self.screen, coord, objects_decor['pos'], objects_decor['type'], objects_decor['variant'],
                           self.tilemap_sprites, self.other_sprite_group, self.all_sprites)
            self.minimun = tile.get_pos()[1] if tile.get_pos()[1] > self.minimun else self.minimun
            if objects_decor['type'] == "player":
                self.hero = Hero(self.screen, self.hero_sprite, self.all_sprites, self.tilemap_sprites, tile.get_pos())
                tile.kill()
                continue
            if objects_decor['type'] == "enemy":
                Enemies(self.screen, self.enemies_sprite_group, self.all_sprites,
                        self.tilemap_sprites, tile.get_pos(), self.check_coord,
                        Gun(self.guns_sprite_group, self.all_sprites))
                tile.kill()
                continue

        for objects in self.tilemap["tilemap"]:
            value_object = self.tilemap['tilemap'][objects]
            coord = 'tilemap'
            Tilemap(self.screen, coord, value_object['pos'], value_object['type'],
                    value_object["variant"], self.tilemap_sprites, self.other_sprite_group, self.all_sprites)

    def generate_map(self, num):
        with open(rf'levels/level_{num}.json', 'r', encoding='utf-8') as file:
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
        self.guns_sprite_group = pygame.sprite.Group()

    def activate_sprites(self):
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
        self.enemies_sprite_group.update(self.hero_sprite)

        self.guns_sprite_group.draw(self.screen)

    def delete_clouds(self):
        for cloud in self.clouds_sprites:
            cloud.kill()

    def draw_clouds(self):
        [Clouds(self.screen, self.clouds_sprites, self.all_sprites) for _ in range(self.start_len_of_clouds)]
        running = True
        while running:
            pygame.mouse.set_visible(False)
            self.clouds_sprites.draw(self.screen)
            self.clouds_speed.update(True)

    def menu(self):
        self.start_button = Menu(self.width / 2 - (200 / 2), self.height - 570, 200, 90, '',
                                 'data/images/buttons/new_start.png',
                                 'data/images/buttons/new_start_hover.png', 'data/sfx/button.mp3')
        self.settings_button = Menu(self.width / 2 - (200 / 2), self.height - 470, 200, 90, '',
                                    'data/images/buttons/settings.png',
                                    'data/images/buttons/settings_hover.png', 'data/sfx/button.mp3')
        self.exit_button = Menu(self.width / 2 - (200 / 2), self.height - 370, 200, 90, '',
                                'data/images/buttons/exit.png',
                                'data/images/buttons/exit_hover.png', 'data/sfx/button.mp3')
        pygame.mouse.set_visible(False)
        menu = True
        while menu:
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))
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
                for btn in [self.start_button, self.settings_button, self.exit_button]:
                    btn.handle_event(event)
            for btn in [self.start_button, self.settings_button, self.exit_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.screen)
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_focused():
                self.screen.blit(self.new_mouse, pos)
            pygame.display.update()

    def settings(self):
        # audio_button = Menu(self.width / 2 - (200 / 2), self.height - 570, 200, 90, '',
        # 'data/images/buttons/audio.png', 'data/images/buttons/audio_hover.png', 'data/sfx/button.mp3')
        video_button = Menu(self.width / 2 - (200 / 2), self.height - 570, 200, 90, '',
                            'data/images/buttons/video.png',
                            'data/images/buttons/video_hover.png', 'data/sfx/button.mp3')
        back_button = Menu(self.width / 2 - (200 / 2), self.height - 470, 200, 90, '',
                           'data/images/buttons/back.png', 'data/images/buttons/back_hover.png', 'data/sfx/button.mp3')
        running = True
        while running:
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))
            font = pygame.font.Font(None, 56)
            text_surface = font.render('', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width / 2, 100))
            self.screen.blit(text_surface, text_rect)
            for event in pygame.event.get():
                if event.type == self.clouds_speed:
                    self.clouds_sprites.update(True)
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
                    for btn in [video_button, back_button]:
                        btn.indent(self.width / 2 - (200 / 2))
                    running = False
                for btn in [video_button, back_button]:
                    btn.handle_event(event)
            for btn in [video_button, back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.screen)
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_focused():
                self.screen.blit(self.new_mouse, pos)
            pygame.display.update()

    def video_settings(self):
        video_mode_1_button = Menu(self.width / 2 - (200 / 2), self.height - 570, 200, 90, '',
                                   'data/images/buttons/800x600.png',
                                   'data/images/buttons/800x600_hover.png', 'data/sfx/button.mp3')
        video_mode_2_button = Menu(self.width / 2 - (200 / 2), self.height - 470, 200, 90, '',
                                   'data/images/buttons/1280x1024.png',
                                   'data/images/buttons/1280x1024_hover.png', 'data/sfx/button.mp3')
        video_mode_3_button = Menu(self.width / 2 - (200 / 2), self.height - 370, 200, 90, '',
                                   'data/images/buttons/full_hd.png',
                                   'data/images/buttons/full_hd_hover.png', 'data/sfx/button.mp3')
        back_button = Menu(self.width / 2 - (200 / 2), self.height - 270, 200, 90, '',
                           'data/images/buttons/back.png',
                           'data/images/buttons/back_hover.png', 'data/sfx/button.mp3')
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
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_focused():
                self.screen.blit(self.new_mouse, pos)
            pygame.display.update()

    def video_mode_update(self, width, height, fullsc=0):
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height), fullsc)
        get_info("update game_info set Resolution = '{}'", f"{width}, {height}", "update")
        self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                (width, height)), (0, 0))

    def restart(self):
        for i in self.tilemap_sprites:
            i.kill()
        for i in self.other_sprite_group:
            i.kill()
        for i in self.enemies_sprite_group:
            i.kill()
        for i in self.guns_sprite_group:
            i.kill()
        for i in self.hero_sprite:
            i.kill()

    def run(self):
        pygame.mouse.set_visible(False)
        is_running = True
        camera = Camera(self.screen)
        pygame.time.set_timer(self.clouds_speed, 100)
        [Clouds(self.screen, self.clouds_sprites, self.all_sprites) for _ in range(self.start_len_of_clouds)]
        while is_running:
            if self.hero.rect.y >= 900:
                self.restart()
                self.tilemap = self.generate_map(self.count_of_map)
                self.render_map()
                self.transition = -50
            if self.hero.is_hero_death:
                self.restart()
                self.count_of_map = get_info("select Level from game_info", type_of_request="get")
                self.tilemap = self.generate_map(self.count_of_map)
                self.render_map()
                self.transition = -50
                self.hero.is_hero_death = False
            if len(self.enemies_sprite_group) == 0:
                self.restart()
                self.count_of_map += 1
                get_info(f"update game_info set Level = {self.count_of_map}", type_of_request="update")
                self.tilemap = self.generate_map(self.count_of_map)
                self.render_map()
                self.transition = -50
            if self.count_of_map == 4:
                self.count_of_map = 1
                get_info(f"update game_info set Level = {self.count_of_map}", type_of_request="update")
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"),
                                                    (self.width, self.height)), (0, 0))
            pygame.mouse.set_visible(False)
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
                self.hero.update(self.enemies_sprite_group, event=event)
            [Particles(self.screen, "leaf", self.particles, self.horizontal_borders, self.vertical_borders,
                       self.all_sprites) for _ in range(self.start_len_of_particles - len(self.particles))]
            camera.update(self.hero)
            for sprite in self.all_sprites:
                camera.apply(sprite)
            self.update_sprites()
            if self.transition < 0:
                self.transition += 1
            if self.transition:
                transition_surf = pygame.Surface(self.screen.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.screen.get_width() // 2,
                                   self.screen.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.screen.blit(transition_surf, (0, 0))
            self.fps.tick(80)
            pygame.display.update()


if __name__ == "__main__":
    Game().menu()

import sys

from CharactersPhysics import Hero

from image_loader import load_image

import pygame


class Game:
    def __init__(self):
        self.width, self.height = 600, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = pygame.time.Clock()
        self.hero_sprite = pygame.sprite.Group()
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
            self.fps.tick(100)
            pygame.display.update()


Game().run()

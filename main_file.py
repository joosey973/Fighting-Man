import pygame
import sys


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((600, 600))
        self.fps = pygame.time.Clock()

    def run(self):
        is_running = True
        while is_running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.fps.tick(60)
            pygame.display.update()
        


Game().run()
                
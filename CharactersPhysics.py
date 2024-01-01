import pygame

from image_loader import load_image


class Hero(pygame.sprite.Sprite):
    def __init__(self, *sprite):
        super().__init__(*sprite)
        self.image = pygame.transform.scale(load_image("images/entities/player.png", -1), (32, 60))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 300
        self.dx = 10
        self.dy = 5

    def update(self, *args):
        if args:
            key = args[0]
            if key[pygame.K_d]:
                self.rect.right += self.dx
            if key[pygame.K_a]:
                self.rect.left -= self.dx
            if key[pygame.K_w]:
                self.rect.top -= self.dy
            if key[pygame.K_s]:
                self.rect.bottom += self.dy

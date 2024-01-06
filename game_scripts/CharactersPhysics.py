from image_loader import load_image

import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, *sprite):
        super().__init__(*sprite)
        self.index_of_hero_static_img = 0
        self.index = 0
        self.image = pygame.transform.scale(load_image(f"images\entities\player\idle\{self.index_of_hero_static_img}.png", -1), (70, 90))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 300
        self.dx = 10
        self.dy = 5

    def update(self, *args):
        if not args:
            self.image = pygame.transform.scale(load_image(f"images\entities\player\idle\{self.index_of_hero_static_img}.png", -1), (70, 90))
            if self.index == 50:
                self.index_of_hero_static_img += 1
                self.index = 0
            if self.index_of_hero_static_img == 21:
                self.index_of_hero_static_img = 0
            self.index += 1
        elif args:
            key = args[0]
            if key[pygame.K_d]:
                self.rect.right += self.dx
            if key[pygame.K_a]:
                self.rect.left -= self.dx
            if key[pygame.K_w]:
                self.rect.top -= self.dy
            if key[pygame.K_s]:
                self.rect.bottom += self.dy

import sys

from CharactersPhysics import Hero

from image_loader import load_image

import pygame


# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, sprite_group):
#         super().__init__(sprite_group)
#         self.frames = []
#         self.cut_sheet(sheet, columns, rows)
#         self.cur_frame = 0
#         self.image = self.frames[self.cur_frame]
#         self.rect = self.rect.move(x, y)

#     def cut_sheet(self, sheet, columns, rows):
#         self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 self.frames.append(sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size)))

#     def update(self):
#         self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#         self.image = self.frames[self.cur_frame]


class Game:
    def __init__(self):
        self.width, self.height = 600, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = pygame.time.Clock()
        self.hero_sprite = pygame.sprite.Group()
        Hero(self.hero_sprite)

    def run(self):
        is_running = True
        while is_running:
            self.screen.blit(pygame.transform.scale(load_image("images/background.png"), (self.width, self.height)), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                key = pygame.key.get_pressed()
                self.hero_sprite.update(key)
            self.hero_sprite.update()
            self.hero_sprite.draw(self.screen)
            self.fps.tick(200)
            pygame.display.update()


Game().run()

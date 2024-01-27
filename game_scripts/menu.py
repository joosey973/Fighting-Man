import pygame


class Menu:
    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None, sound_path=None) -> None:
        pygame.mixer.init()
        pygame.font.init()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert(), (width, height))
        self.image.set_colorkey((255, 255, 255))
        self.hover = self.image
        if hover_image_path:
            self.hover = pygame.transform.scale(pygame.image.load(hover_image_path).convert(), (width, height))
            self.hover.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def indent(self, x, y=None):
        self.x = x
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        current_image = self.hover if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)
        if self.text:
            font = pygame.font.Font(None, 56)
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

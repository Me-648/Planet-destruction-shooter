# planet.py
import pygame
import random

class Planet(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.image = pygame.Surface([40, 40])
        self.image.fill((150, 75, 0)) # 茶色

        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = -self.rect.height

        self.speed = random.randrange(1, 5)
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > self.screen_height:
            self.kill()
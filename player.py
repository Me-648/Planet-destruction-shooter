# player.py
import pygame
from shot import Shot

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, keys_left, keys_right, keys_up, keys_down, speed, screen_width, screen_height):
        super().__init__()

        self.image = pygame.Surface([50, 50])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.color = color
        self.speed = speed

        self.keys_left = keys_left
        self.keys_right = keys_right
        self.keys_up = keys_up
        self.keys_down = keys_down

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.min_y = self.screen_height // 2
        self.max_y = self.screen_height - self.rect.height

    def update(self, keys):
        if keys[self.keys_left]:
            self.rect.x -= self.speed
        if keys[self.keys_right]:
            self.rect.x += self.speed
        if keys[self.keys_up]:
            self.rect.y -= self.speed
        if keys[self.keys_down]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(self.min_y, min(self.rect.y, self.max_y))

    def shoot(self):
        new_shot = Shot(self.rect.centerx, self.rect.top, self.color)
        return new_shot
# planet.py
import pygame
import random

class BasePlanet(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, size, color, speed, hp):
        super().__init__()

        self.image = pygame.Surface([size, size])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = -self.rect.height

        self.speed = speed
        self.hp = hp
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed

        # 画面下まで行ったら消える
        if self.rect.y > self.screen_height:
            self.kill()

    def take_damage(self, damage_amount):
        self.hp -= damage_amount
        if self.hp <= 0:
            self.kill()

    # 惑星が破壊されたときに特別な処理を行うためのメソッド (デフォルトは何もしない)
    def on_destroyed(self):
        pass
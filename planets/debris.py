import pygame
import random
import os

class Debris(pygame.sprite.Sprite):
  def __init__(self, x, y, screen_width, screen_height):
    super().__init__()
    image_path = os.path.join('assets', 'images', 'planets', 'rock_debris.png')
    size = random.randint(30, 40)
    color = (150, 150, 150)

    self.screen_width = screen_width
    self.screen_height = screen_height

    # 破片が与えるダメージ量
    self.damage_amount = 1

    if os.path.exists(image_path):
      self.image = pygame.image.load(image_path).convert_alpha()
      self.image = pygame.transform.scale(self.image, (size, size))
    else:
      print(f"Warning: Debris image not found at {image_path}. Using default square.")
      self.image = pygame.Surface((size, size), pygame.SRCALPHA)
      pygame.draw.rect(self.image, color, self.image.get_rect())

    self.rect = self.image.get_rect(center=(x, y))

    # 破片の移動方向と速度
    # 360°のランダムな角度にランダムな速度で飛び散る
    angle = random.uniform(0, 360)
    speed = random.uniform(2, 5)
    self.vx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
    self.vy = speed * pygame.math.Vector2(1, 0).rotate(angle).y

  def update(self):
    self.rect.x += self.vx
    self.rect.y += self.vy

    # 画面外に出たら消滅
    if (self.rect.right < 0 or self.rect.left > self.screen_width or
        self.rect.bottom < 0 or self.rect.top > self.screen_height):
      self.kill()
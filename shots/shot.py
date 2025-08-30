import pygame
import os
import math

class Shot(pygame.sprite.Sprite):
  def __init__(self, x, y, color, owner_player=None, damage=1, shot_type="normal", vx=0, vy=15):
    super().__init__()

    self.owner_player = owner_player
    self.damage = damage
    self.shot_type = shot_type

    self.vx = vx
    self.vy = vy

    image_path = None
    if self.shot_type == "normal":
      image_path = os.path.join('assets', 'images', 'shots', 'shot_normal.png')
      shot_width = 5
      shot_height = 15
    elif self.shot_type == "power":
      image_path = os.path.join('assets', 'images', 'shots', 'shot_power.png')
      shot_width = 10
      shot_height = 18
    elif self.shot_type == "triple":
      image_path = os.path.join('assets', 'images', 'shots', 'shot_triple.png')
      shot_width = 8
      shot_height = 16
    else:
      image_path = os.path.join('assets', 'images', 'shots', 'shot_normal.png')
      shot_width = 5
      shot_height = 15
      self.speed = -15
      print(f"ショットタイプがない: {shot_type}. デフォルトのノーマルショット使います")

    if os.path.exists(image_path):
      original_image = pygame.image.load(image_path).convert_alpha()
      self.image = pygame.transform.scale(original_image, (shot_width, shot_height))
    else:
      print(f"ショット画像がないよ: {image_path}. 代替の四角いショットを使用します。")
      if self.shot_type == "power":
        self.image = pygame.Surface([5, 15])
        self.image.fill((255, 255, 0))
      elif self.shot_type == "triple":
        self.image = pygame.Surface([5, 15])
        self.image.fill((0, 255, 255))
      else:
        self.image = pygame.Surface([5, 15])
        self.image.fill(color)
    self.rect = self.image.get_rect(center=(x, y))

  def update(self):
    # ショットを移動させる
    self.rect.x += self.vx
    self.rect.y += self.vy
        
    # 画面上部まで行ったら消える
    if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
      self.kill()
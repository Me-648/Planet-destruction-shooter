import pygame
import os
import math

class Shot(pygame.sprite.Sprite):
  def __init__(self, x, y, owner_player=None, damage=1, vx=0, vy=15, image_path=None, size=(5, 15), color=(255, 255, 255)):
    super().__init__()

    self.owner_player = owner_player
    self.damage = damage

    self.vx = vx
    self.vy = vy

    if image_path and os.path.exists(image_path):
      original_image = pygame.image.load(image_path).convert_alpha()
      self.image = pygame.transform.scale(original_image, size)
    else:
      print(f"ショット画像がないよ: {image_path}. 代替の四角いショットを使用します。")
      self.image = pygame.Surface(size)
      self.image.fill(color)
    
    self.rect = self.image.get_rect(center=(x, y))

  def update(self):
    # ショットを移動させる
    self.rect.x += self.vx
    self.rect.y += self.vy
        
    # 画面上部まで行ったら消える
    if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
      self.kill()
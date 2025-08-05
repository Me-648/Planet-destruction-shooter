import pygame
import os

class MidBossShot(pygame.sprite.Sprite):
  def __init__(self, x, y, direction_x, direction_y, damage):
    super().__init__()

    shot_image_path = os.path.join('assets', 'images', 'shots', 'shot_mid_boss.png') # 新しい画像パス
    if os.path.exists(shot_image_path):
      original_image = pygame.image.load(shot_image_path).convert_alpha()
      self.image = pygame.transform.scale(original_image, (30, 30)) # サイズを少し大きくする
    else:
      print(f"Warning: Mid Boss shot image not found. Using red square.")
      self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
      pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 30, 30)) # 赤い四角

    self.rect = self.image.get_rect(center=(x, y))
    
    self.speed = 4  # 速度を調整
    self.damage = damage

    self.direction_x = direction_x
    self.direction_y = direction_y
  
  def update(self):
    self.rect.x += self.direction_x * self.speed
    self.rect.y += self.direction_y * self.speed

    screen_rect = pygame.display.get_surface().get_rect()
    if not screen_rect.colliderect(self.rect):
      self.kill()
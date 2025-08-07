import pygame
import os

class MidBossShot(pygame.sprite.Sprite):
  def __init__(self, x, y, direction_x, direction_y, damage, image_path):
    super().__init__()

    full_image_path = os.path.join(image_path)
    if os.path.exists(full_image_path):
      original_image = pygame.image.load(full_image_path).convert_alpha()
      self.image = pygame.transform.scale(original_image, (30, 30)) # サイズを少し大きくする
    else:
      print(f"Warning: Mid Boss shot image not found. Path: {full_image_path}. Using red square.")
      self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
      pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 30, 30))

    self.rect = self.image.get_rect(center=(x, y))
    
    self.speed = 4
    self.damage = damage

    self.direction_x = direction_x
    self.direction_y = direction_y
  
  def update(self):
    self.rect.x += self.direction_x * self.speed
    self.rect.y += self.direction_y * self.speed

    screen_rect = pygame.display.get_surface().get_rect()
    if not screen_rect.colliderect(self.rect):
      self.kill()
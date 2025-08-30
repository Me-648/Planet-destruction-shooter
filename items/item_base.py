import pygame
import os
import random

class BaseItem(pygame.sprite.Sprite):
  def __init__(self, screen_width, screen_height, size, image_path=None):
    super().__init__()

    if image_path:
      original_image = pygame.image.load(os.path.join('assets', 'images', image_path)).convert_alpha()
      self.image = pygame.transform.scale(original_image, (size, size))
    else:
      self.image = pygame.Surface([size, size])
      self.image.fill((255, 255, 0))

    self.rect = self.image.get_rect()

    self.rect.x = random.randrange(screen_width - self.rect.width)
    self.rect.y = -self.rect.height

    self.speed = 2
    self.screen_height = screen_height
    self.screen_width = screen_width
  
  def update(self):
    self.rect.y += self.speed

    if self.rect.y > self.screen_height:
      self.kill()

  def apply_effect(self, player_instance, game_screen_instance):
    pass
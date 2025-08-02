import pygame
import random
import os

class BasePlanet(pygame.sprite.Sprite):
  def __init__(self, screen_width, screen_height, size, color, hp, speed, score_value, image_path=None):
    super().__init__()

    if image_path:
      original_image = pygame.image.load(os.path.join('assets', 'images', image_path)).convert_alpha()
      self.image = pygame.transform.scale(original_image, (size, size))
    else:
      self.image = pygame.Surface([size, size])
      self.image.fill(color)

    self.rect = self.image.get_rect()

    self.rect.x = random.randrange(screen_width - self.rect.width)
    self.rect.y = -self.rect.height

    self.speed = speed
    self.speed_x = 0
    self.speed_y = speed
    self.hp = hp
    self.score_value = score_value
    self.screen_height = screen_height
    self.screen_width = screen_width

    self.destroyed = False

  def update(self, game_screen=None):
    if game_screen and game_screen.is_planet_slowdown_active:
        slowdown_factor = game_screen.planet_slowdown_factor
    else:
        slowdown_factor = 1.0

    self.rect.x += self.speed_x * slowdown_factor
    self.rect.y += self.speed_y * slowdown_factor

    # 画面下まで行ったら消える
    if self.rect.y > self.screen_height:
      self.kill()

  def take_damage(self, damage_amount):
    self.hp -= damage_amount
    if self.hp <= 0:
      self.kill()
      self.destroyed = True
      return True # 破壊されたらTrue
    return False

  # 惑星が破壊されたときに特別な処理を行うためのメソッド (デフォルトは何もしない)
  def on_destroyed(self, game_screen_instance, destroying_player):
    pass
import pygame
import random
from .planet_base import BasePlanet

class PenaltyPlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 60
    color = (200, 50, 50)
    speed = random.uniform(1.0, 2.5)
    hp = 3

    score_value = -50

    image_paths = [
      'planet_penalty_1.png',
      'planet_penalty_2.png',
      'planet_penalty_3.png',
    ]

    selected_image_path = random.choice(image_paths)
    
    super().__init__(screen_width, screen_height, size, color, hp, speed, score_value, selected_image_path)

    self.original_image = self.image.copy()
    self.angle = 0
    self.rotation_speed = random.choice([-3, -2, 2, 3])

  def update(self):
    super().update()

    self.angle = (self.angle + self.rotation_speed) % 360

    current_center = self.rect.center
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect(center=current_center)

  def on_destroyed(self, game_screen_instance, destroying_player):
    print("惑星...？が破壊されました！スコアが減少します。")
    if destroying_player:
      print(f"{destroying_player.color}プレイヤーのスコアが50減少しました！合計: {destroying_player.score}")
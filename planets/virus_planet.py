import random
from .planet_base import BasePlanet

class VirusPlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 60
    color = (0, 150, 0)
    speed = random.uniform(1.5, 3.0)
    hp = 5
    score_value = 0

    image_path = 'planets/planet_virus.png'

    super().__init__(screen_width, screen_height, size, color, hp, speed, score_value, image_path)

    self.player_damage_on_destroy = 1

  def on_destroyed(self, game_screen_instance, destroying_player):
    if destroying_player:
      destroying_player.take_damage(self.player_damage_on_destroy)
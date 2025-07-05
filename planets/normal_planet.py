from .planet_base import BasePlanet
import random

class NormalPlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 40
    color = (150, 75, 0)
    speed = random.uniform(1, 3)
    hp = 1

    score_value = 10
    image_path = 'planet_normal.png'
    super().__init__(screen_width, screen_height, size, color, hp, speed, score_value, image_path)
    
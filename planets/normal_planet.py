from .planet_base import BasePlanet
import random

class NormalPlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 40
    color = (150, 75, 0)
    speed = random.randrange(1, 3)
    hp = 1
    super().__init__(screen_width, screen_height, size, color, speed, hp)
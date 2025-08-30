import random
import os
from .planet_base import BasePlanet

class MidPlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 150
    color = (150, 100, 50)
    speed = random.uniform(1.0, 1.3)
    hp = 30
    score_value = 150

    image_path = 'planets/planet_mid.png'

    super().__init__(screen_width, screen_height, size, color, hp, speed, score_value, image_path)
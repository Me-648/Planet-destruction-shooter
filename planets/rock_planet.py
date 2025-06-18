from .planet_base import BasePlanet
import random

class RockPlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 60
    color = (100, 100, 100)
    speed = random.randrange(2, 4)
    hp = 3
    super().__init__(screen_width, screen_height, size, color, speed, hp)
  
  def on_destroyed(self):
    print("岩石惑星が破壊され、破片をまき散らしました！(まだ実装されていません)")
    pass
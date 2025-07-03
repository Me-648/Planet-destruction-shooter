from .planet_base import BasePlanet
import random

class RockPlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 60
    color = (100, 100, 100)
    speed = random.uniform(0.8, 2)
    hp = 3

    score_value = 30
    image_path = 'planet_rock.png'
    super().__init__(screen_width, screen_height, size, color, hp, speed, score_value, image_path)
  
  def on_destroyed(self):
    print("岩石惑星が破壊され、破片をまき散らしました！(まだ実装されていません)")
    pass
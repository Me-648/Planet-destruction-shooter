from .planet_base import BasePlanet
from .debris import Debris
import random

class RockPlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 70
    color = (100, 100, 100)
    speed = random.uniform(1.1, 2.2)
    hp = 3

    score_value = 30
    image_path = 'planets/planet_rock.png'
    super().__init__(screen_width, screen_height, size, color, hp, speed, score_value, image_path)
  
  def on_destroyed(self, game_screen_instance, destroying_player):
    print(f"岩石惑星破壊！ ID: {id(self)}")
    num_debris = random.randint(3, 5)
    print(f"破片数: {num_debris}")
    for _ in range(num_debris):
      new_debris = Debris(self.rect.centerx, self.rect.centery, game_screen_instance.screen_width, game_screen_instance.screen_height)
      game_screen_instance.all_sprites.add(new_debris)
      game_screen_instance.debris.add(new_debris)
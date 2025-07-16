import random
from .planet_base import BasePlanet

class IcePlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 60
    color = (100, 150, 255)
    speed = random.uniform(2.5, 4.5)
    hp = 2
    score_value = 40

    image_path = 'planets/planet_ice.png'
    
    super().__init__(screen_width, screen_height, size, color, hp, speed, score_value, image_path)
  
  def on_destroyed(self, game_screen_instance, destroying_player):
    print(f"氷惑星が破壊されました！{destroying_player.color if destroying_player else '不明な'}プレイヤーに減速効果を適用します。")
    if destroying_player:
      destroying_player.apply_slow_effect()
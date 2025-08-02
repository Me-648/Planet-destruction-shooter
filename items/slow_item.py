import pygame
import os
from items.item_base import BaseItem

class SlowItem(BaseItem):
  def __init__(self, screen_width, screen_height):
    size = 40
    image_path = 'items/item_slow.png'

    super().__init__(screen_width, screen_height, size, image_path)

    if not os.path.exists(os.path.join('assets', 'images', image_path)):
      self.image.fill((173, 216, 230))

  def apply_effect(self, player_instance, game_screen_instance):
    duration_ms = 7000 # 7秒間
    slow_factor = 0.5
    
    game_screen_instance.activate_planet_slowdown(duration_ms, slow_factor)
    print(f"プレイヤー{player_instance.player_id}がスローアイテムを取得しました！")
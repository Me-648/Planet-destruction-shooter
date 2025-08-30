import pygame
import os
from items.item_base import BaseItem

class SpeedUpItem(BaseItem):
  def __init__(self, screen_width, screen_height):
    size = 40
    image_path = 'items/item_speed_up.png'

    super().__init__(screen_width, screen_height, size, image_path)

    if not os.path.exists(os.path.join('assets', 'images', image_path)):
      self.image.fill((255, 255, 0))

  def apply_effect(self, player_instance, game_screen_instance):
    # 速度アップの効果時間と倍率
    duration_ms = 10000
    speed_multiplier = 1.5

    player_instance.activate_speed_up(duration_ms, speed_multiplier)
    print(f"プレイヤー{player_instance.player_id}が移動速度UPアイテムを取得しました！")
import pygame
import os
from .item_base import BaseItem

class TripleShotItem(BaseItem):
  def __init__(self, screen_width, screen_height):
    size = 40
    image_path = 'items/item_triple_shot.png'
    super().__init__(screen_width, screen_height, size, image_path)

    if not os.path.exists(os.path.join('assets', 'images', image_path)):
      self.image.fill((0, 255, 255))

  def apply_effect(self, player_instance, game_screen_instance):
    triple_shot_duration_ms = 10000

    if not player_instance.has_active_triple_shot():
      player_instance.activate_triple_shot(triple_shot_duration_ms)
      print(f"プレイヤー{player_instance.player_id}が三方向ショットアイテムを取得しました！")
    else:
      print(f"プレイヤー{player_instance.player_id}は既に三方向ショットを持っています。時間を延長します！")
      player_instance.activate_triple_shot(triple_shot_duration_ms)
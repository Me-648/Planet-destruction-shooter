import pygame
import os
from items.item_base import BaseItem

class InvincibilityItem(BaseItem):
  def __init__(self, screen_width, screen_height):
    size = 40
    image_path = 'items/item_invincibility.png'

    super().__init__(screen_width, screen_height, size, image_path)

    if not os.path.exists(os.path.join('assets', 'images', image_path)):
      self.image.fill((255, 255, 255))

  def apply_effect(self, player_instance, game_screen_instance):
    duration_ms = 777 * 10
    
    player_instance.activate_invincibility(duration_ms)
    print(f"プレイヤー{player_instance.player_id}が無敵アイテムを取得しました！")
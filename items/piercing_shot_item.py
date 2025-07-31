import pygame
import os
from .item_base import BaseItem

class PiercingShotItem(BaseItem):
  def __init__(self, screen_width, screen_height):
    size = 40
    image_path = 'items/item_piercing_shot.png'

    super().__init__(screen_width, screen_height, size, image_path)

  def apply_effect(self, player_instance, game_screen_instance):
    num_uses = player_instance.piercing_shot_max_uses
    player_instance.activate_piercing_shot(num_uses)
    print(f"プレイヤー{player_instance.player_id}が貫通ショットアイテムを取得しました！残り {num_uses} 発")
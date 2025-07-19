import pygame
from .item_base import BaseItem

class BarrierItem(BaseItem):
  def __init__(self, screen_width, screen_height):
    size = 40
    image_path = 'items/item_barrier.png'

    super().__init__(screen_width, screen_height, size, image_path)

  def apply_effect(self, player_instance, game_screen_instance):
    if not player_instance.has_active_barrier():
      player_instance.activate_barrier()
      print(f"プレイヤー{player_instance.player_id}がバリアアイテムを取得しました！")
    else:
      print(f"プレイヤー{player_instance.player_id}は既にバリアを持っています。")
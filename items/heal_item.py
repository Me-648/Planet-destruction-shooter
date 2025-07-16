import pygame
from .item_base import BaseItem

class HealItem(BaseItem):
  def __init__(self, screen_width, screen_height):
    size = 40
    image_path = 'items/item_heal.png'
    super().__init__(screen_width, screen_height, size, image_path)

    # 回復量
    self.heal_amount = 1
  
  def apply_effect(self, player_instance, game_screen_instance):
    max_hp = 3

    # 最大HPを超えないように回復
    if player_instance.hp < max_hp:
      player_instance.hp += self.heal_amount
      if player_instance.hp > max_hp:
        player_instance.hp = max_hp
      print(f"プレイヤー{player_instance.player_id}が回復アイテムを取得！HPが{self.heal_amount}回復しました。現在HP: {player_instance.hp}")
    else:
      print(f"プレイヤー{player_instance.player_id}は既に最大HPです。")
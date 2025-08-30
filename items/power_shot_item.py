from .item_base import BaseItem

class PowerShotItem(BaseItem):
  def __init__(self, screen_width, screen_height):
    size = 40
    image_path = 'items/item_powershot.png'
    super().__init__(screen_width, screen_height, size, image_path)

    # 効果時間(ミリ秒)
    self.duration = 10000
    # ダメージ倍率
    self.damage_multiplier = 5

  def apply_effect(self, player_instance, game_screen_instance):
    player_instance.apply_power_shot(self.damage_multiplier, self.duration)
    print(f"プレイヤー{player_instance.player_id}がパワーショットアイテムを取得！{self.duration/1000}秒間、ショット威力が{self.damage_multiplier}倍になります。")
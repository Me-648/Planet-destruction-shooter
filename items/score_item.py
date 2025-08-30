import random
from .item_base import BaseItem

class ScoreItem(BaseItem):
  def __init__(self, screen_width, screen_height):

    size = 40
    image_path = 'items/item_score.png'

    super().__init__(screen_width, screen_height, size, image_path)

    self.score_value = random.choice([50, 100, 200])

  def apply_effect(self, player_instance, game_screen_instance):
    player_instance.add_score(self.score_value)
    print(f"プレイヤー{player_instance.player_id}がスコアアイテムを取得！スコアが{self.score_value}増えました。現在のスコア: {player_instance.score}")
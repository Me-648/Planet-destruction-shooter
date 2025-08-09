from .item_base import BaseItem

class BarrierItem(BaseItem):
  def __init__(self, screen_width, screen_height):
    size = 40
    image_path = 'items/item_barrier.png'

    super().__init__(screen_width, screen_height, size, image_path)

  def apply_effect(self, player_instance, game_screen_instance):
    if player_instance.barrier_count < player_instance.max_barrier_count:
      player_instance.activate_barrier()
      print(f"プレイヤー{player_instance.player_id}がバリアアイテムを取得しました！（バリア再展開）")
    else:
      print(f"プレイヤー{player_instance.player_id}のバリアは既に最大です。")
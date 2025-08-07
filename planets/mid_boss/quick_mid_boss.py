import os
from planets.mid_boss.mid_boss import MidBoss

class QuickMidBoss(MidBoss):
  # HPが低く、移動速度が速い中ボス
  def __init__(self, screen_width, screen_height):
    super().__init__(
      screen_width, 
      screen_height,
      image_path='mid_boss/quick_mid_boss.png',
      hp = 50,
      speed_x = 4,
      shoot_cooldown = 1000,
      score_value = 1000,
      damage_amount = 2,
      size=(200, 200)
    )
    self.shot_image_path = os.path.join("assets", "images", "shots", "shot_quick_mid_boss.png")
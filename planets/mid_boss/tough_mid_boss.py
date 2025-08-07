import os
from planets.mid_boss.mid_boss import MidBoss

class ToughMidBoss(MidBoss):
  def __init__(self, screen_width, screen_height):
    super().__init__(
      screen_width, 
      screen_height,
      image_path='mid_boss/tough_mid_boss.png', 
      hp = 200, 
      speed_x = 1,
      shoot_cooldown = 1500,
      score_value = 1000,
      damage_amount = 2,
      size=(300, 300) 
    )
    self.shot_image_path = os.path.join("assets", "images", "shots", "shot_tough_mid_boss.png")
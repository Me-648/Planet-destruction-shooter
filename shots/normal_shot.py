import os
from shots.base_shot import Shot

class NormalShot(Shot):
  def __init__(self, x, y, owner_player=None, is_power_active=False):
    image_path = os.path.join('assets', 'images', 'shots', 'shot_normal.png')
    size = (5, 15)
    color = (255, 255, 255)
    damage = 1
    if is_power_active:
      damage = 2
    vx = 0
    vy = -15

    super().__init__(x, y, owner_player=owner_player, damage=damage, vx=vx, vy=vy, image_path=image_path, size=size, color=color)
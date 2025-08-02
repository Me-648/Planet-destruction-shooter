import os
from shots.base_shot import Shot

class PiercingShot(Shot):
  def __init__(self, x, y, owner_player=None, is_power_active=False):
    image_path = os.path.join('assets', 'images', 'shots', 'shot_piercing.png')
    size = (24, 130)
    color = (200, 0, 255)
    damage = 100
    if is_power_active:
      damage *= 2

    vx = 0
    vy = -15

    super().__init__(x, y, owner_player, damage, vx, vy, image_path, size, color)

    self.hit_enemies = set()
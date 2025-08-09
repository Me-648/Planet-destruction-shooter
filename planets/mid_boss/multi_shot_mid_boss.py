import math
import os
from planets.mid_boss.mid_boss import MidBoss
from shots.mid_boss_shot import MidBossShot

class MultiShotMidBoss(MidBoss):
  def __init__(self, screen_width, screen_height):
    super().__init__(
      screen_width, 
      screen_height,
      image_path='mid_boss/multi_shot_mid_boss.png',
      hp = 150,
      speed_x = 2,
      shoot_cooldown = 2000,
      score_value = 1000,
      damage_amount = 2,
      size=(250, 250)
    )
    self.shot_image_path = os.path.join("assets", "images", "shots", "shot_multi_shot_mid_boss.png")
    
  def shoot(self, game_screen):
    target_players = [p for p in game_screen.players if p.is_alive()]
    if not target_players:
      return

    target_player = min(target_players, key=lambda p: (self.rect.centerx - p.rect.centerx)**2 + (self.rect.centery - p.rect.centery)**2)
        
    angles = [-20, 0, 20]
    for angle_deg in angles:
      direction_x = target_player.rect.centerx - self.rect.centerx
      direction_y = target_player.rect.centery - self.rect.centery
            
      angle_rad = math.atan2(direction_y, direction_x) + math.radians(angle_deg)

      new_direction_x = math.cos(angle_rad)
      new_direction_y = math.sin(angle_rad)

      enemy_shot = MidBossShot(self.rect.centerx, self.rect.bottom, new_direction_x, new_direction_y, self.damage_amount, self.shot_image_path)
      game_screen.all_sprites.add(enemy_shot)
      game_screen.enemy_shots.add(enemy_shot)
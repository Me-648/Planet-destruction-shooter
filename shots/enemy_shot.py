import pygame
import os

class EnemyShot(pygame.sprite.Sprite):
  def __init__(self, x, y, speed, target_player_rect):
    super().__init__()

    shot_image_path = os.path.join('assets', 'images', 'shots', 'shot_enemy.png') 
    if os.path.exists(shot_image_path):
            original_image = pygame.image.load(shot_image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (20, 20)) # 弾のサイズを設定
    else:
            print(f"Warning: Enemy shot image not found at {shot_image_path}. Using red circle.")
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 100, 100, 200), (10, 10), 10)

    self.rect = self.image.get_rect(center=(x, y))
    self.speed = speed
    self.damage = 1

    # ターゲットとなるプレイヤーの位置を追跡
    self.target_player_rect = target_player_rect
    self.direction_vector = pygame.math.Vector2(self.target_player_rect.centerx - self.rect.centerx, self.target_player_rect.centery - self.rect.centery)
    if self.direction_vector.length() > 0:
      self.direction_vector = self.direction_vector.normalize()
  
  def update(self):
    # ターゲットに向かって移動
    self.rect.x += self.direction_vector.x * self.speed
    self.rect.y += self.direction_vector.y * self.speed

    # 画面外に出たら消える
    if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height() or self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
      self.kill()
import pygame
import os
from shots.mid_boss_shot import MidBossShot

class MidBoss(pygame.sprite.Sprite):
  def __init__(self, screen_width, screen_height, image_path='mid_boss/original_mid_boss.png', hp=100, speed_x=2, shoot_cooldown=1000, score_value=500, damage_amount=1, size=(250, 250)):
    super().__init__()
    self.screen_width = screen_width
    self.screen_height = screen_height

    # 画像のロード
    full_image_path = os.path.join('assets', 'images', 'planets', image_path)
    if os.path.exists(full_image_path):
      original_image = pygame.image.load(full_image_path).convert_alpha()
      self.image = pygame.transform.scale(original_image, size)
    else:
      print(f"中ボス画像が見つかりません: {full_image_path}")
      self.image = pygame.Surface(size)
      self.image.fill((255, 255, 0))

    # デフォルトのショット画像パスを設定
    self.shot_image_path = os.path.join("assets", "images", "shots", "enemy_shot.png")

    self.rect = self.image.get_rect()

    # 初期位置（画面上部中央）
    self.rect.centerx = self.screen_width // 2
    self.rect.top = -self.rect.height

    # ステータス
    self.hp = hp
    self.max_hp = hp
    self.speed = 1
    self.speed_x = speed_x
    self.damage_amount = damage_amount
    self.score_value = score_value

    # 登場アニメーション用
    self.is_entering = True
    self.target_y = self.screen_height // 8
    
    # 攻撃関連のプロパティを初期化
    self.shoot_cooldown = shoot_cooldown
    self.last_shot_time = pygame.time.get_ticks()

    # 倒されたかどうかのフラグ
    self.is_destroyed = False

  def update(self, game_screen):
    # 登場アニメーション
    if self.is_entering:
      if self.rect.y < self.target_y:
        self.rect.y += self.speed
      else:
        self.is_entering = False
    else:
      # 左右に移動するロジック
      self.rect.x += self.speed_x
      if self.rect.right > game_screen.screen_width or self.rect.left < 0:
        self.speed_x *= -1
    
      # ここに攻撃ロジックを追加する
      current_time = pygame.time.get_ticks()
      if current_time - self.last_shot_time > self.shoot_cooldown:
        self.last_shot_time = current_time
        self.shoot(game_screen)
    
  def draw_hp_bar(self, screen):
    if self.hp > 0:
      bar_width = self.rect.width
      bar_height = 12
      bar_x = self.rect.x
      bar_y = self.rect.y - bar_height - 8
        
      # 背景のバー（暗いグレー）
      pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
        
      # HP割合を計算
      hp_ratio = self.hp / self.max_hp
      current_bar_width = hp_ratio * bar_width
        
      # HP割合に応じて色を決定
      if hp_ratio > 0.7:
        # 70%以上：緑色
        hp_color = (0, 255, 0)
      elif hp_ratio > 0.4:
        # 40-70%：黄色
        hp_color = (255, 255, 0)
      elif hp_ratio > 0.2:
        # 20-40%：オレンジ
        hp_color = (255, 165, 0)
      else:
        # 20%以下：赤色
        hp_color = (255, 0, 0)
        
      # 現在のHPのバー
      if current_bar_width > 0:
        pygame.draw.rect(screen, hp_color, (bar_x, bar_y, current_bar_width, bar_height))
        

  def take_damage(self, damage):
    if self.is_destroyed:
      return False
    
    self.hp -= damage
    if self.hp <= 0:
      self.hp = 0
      self.is_destroyed = True
      self.kill()
      return True
    return False
  
  def shoot(self, game_screen):
    # 中ボスがプレイヤーを狙って弾を発射する処理
    target_players = [p for p in game_screen.players if p.is_alive()]
    if not target_players:
      return

    target_player = min(target_players, key=lambda p: (self.rect.centerx - p.rect.centerx)**2 + (self.rect.centery - p.rect.centery)**2)
    
    direction_x = target_player.rect.centerx - self.rect.centerx
    direction_y = target_player.rect.centery - self.rect.centery
    
    length = (direction_x**2 + direction_y**2)**0.5
    if length != 0:
      direction_x /= length
      direction_y /= length
    
    # 弾の生成
    enemy_shot = MidBossShot(self.rect.centerx, self.rect.bottom, direction_x, direction_y, self.damage_amount, self.shot_image_path)
    game_screen.all_sprites.add(enemy_shot)
    game_screen.enemy_shots.add(enemy_shot)
  
  def on_destroyed(self, game_screen, destroying_player):
    # 中ボスが破壊されたときの処理
    if not self.is_destroyed:
      print("中ボスを倒しました！")
      # スコア加算
      if destroying_player:
        destroying_player.score += self.score_value
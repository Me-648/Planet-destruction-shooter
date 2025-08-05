import pygame
import os
from shots.mid_boss_shot import MidBossShot

class MidBoss(pygame.sprite.Sprite):
  def __init__(self, screen_width, screen_height):
    super().__init__()
    self.screen_width = screen_width
    self.screen_height = screen_height

    # 中ボス画像のロード
    image_path = os.path.join('assets', 'images', 'planets', 'mid_boss.png')
    if os.path.exists(image_path):
      original_image = pygame.image.load(image_path).convert_alpha()
      # 中ボスのサイズを調整
      self.image = pygame.transform.scale(original_image, (250, 250))
    else:
      print(f"中ボス画像が見つかりません: {image_path}")
      self.image = pygame.Surface([200, 200])
      self.image.fill((255, 255, 0))

    self.rect = self.image.get_rect()

    # 初期位置（画面上部中央）
    self.rect.centerx = self.screen_width // 2
    self.rect.top = -self.rect.height

    # 中ボスの初期ステータス
    self.hp = 100
    self.max_hp = 100
    self.speed = 1
    self.speed_x = 2
    self.damage_amount = 2
    self.score_value = 500

    # 登場アニメーション用
    self.is_entering = True
    self.target_y = self.screen_height // 8
    
    # 左右移動用に追加
    self.speed_x = 2
    # 攻撃関連のプロパティを初期化
    self.shoot_cooldown = 1000
    self.last_shot_time = pygame.time.get_ticks()

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
    # 体力バーを描画するメソッド
    if self.hp > 0:
      bar_width = self.rect.width
      bar_height = 10
      bar_x = self.rect.x
      bar_y = self.rect.y - bar_height - 5
      
      # 背景のバー（灰色）
      pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
      
      # 現在のHPのバー（赤色）
      hp_bar_width = (self.hp / self.max_hp) * bar_width
      pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, hp_bar_width, bar_height))

  def take_damage(self, damage):
    self.hp -= damage
    if self.hp <= 0:
      self.hp = 0
      self.kill() # 体力が0になったらスプライトを削除
      return True
    return False
  
  def shoot(self, game_screen):
    """中ボスがプレイヤーを狙って弾を発射する処理"""
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
    enemy_shot = MidBossShot(self.rect.centerx, self.rect.bottom, direction_x, direction_y, self.damage_amount)
    game_screen.all_sprites.add(enemy_shot)
    game_screen.enemy_shots.add(enemy_shot)
  
  def on_destroyed(self, game_screen, destroying_player):
    """中ボスが破壊されたときの処理"""
    print("中ボスを倒しました！")
    # スコア加算
    if destroying_player:
      destroying_player.score += self.score_value
import pygame
import os
from shots.shot import Shot

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, color, keys_left, keys_right, keys_up, keys_down, speed, screen_width, screen_height, player_id):
    super().__init__()

    self.image = pygame.Surface([50, 50])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

    self.original_image = self.image.copy()

    self.color = color
    self.speed = speed
    self.original_speed = speed

    # 減速効果用
    self.is_slowed = False
    self.slow_start_time = 0
    # 5秒間だけ0.3倍の速度になる
    self.slow_duration = 5000
    self.slow_factor = 0.3

    self.score = 0
    self.hp = 3
    self.max_hp = 3

    # 無敵時間
    self.last_hit_time = 0
    self.invicibility_duration = 1500
    self.is_invincible_blinking = False
    self.blink_interval = 100
    self.last_blink_time = 0
    self.is_visible = True

    self.keys_left = keys_left
    self.keys_right = keys_right
    self.keys_up = keys_up
    self.keys_down = keys_down

    self.screen_width = screen_width
    self.screen_height = screen_height

    self.min_y = self.screen_height // 2
    self.max_y = self.screen_height - self.rect.height

    self.shoot_delay = 20
    self.last_shot_time = 0

    # プレイヤーID
    self.player_id = player_id

    # 効果音のロード
    self.shot_sound = None
    self.hit_sound = None
    shot_sound_path = os.path.join('assets', 'sounds', 'shot.mp3')
    player_hit_sound_path = os.path.join('assets', 'sounds', 'player_hit.mp3')
    if os.path.exists(shot_sound_path):
      self.shot_sound = pygame.mixer.Sound(shot_sound_path)
      self.shot_sound.set_volume(0.2)
    else:
      print(f"発射音がないよ: {shot_sound_path}")
    if os.path.exists(player_hit_sound_path):
      self.hit_sound = pygame.mixer.Sound(player_hit_sound_path)
      self.hit_sound.set_volume(0.2)
    else:
      print(f"プレイヤーヒット音がないよ: {player_hit_sound_path}")

    
    # パワーショット(アイテム)関連のプロパティ
    self.is_power_shot_active = False
    self.power_shot_start_time = 0
    self.power_shot_duration = 0
    self.current_damage_multiplier = 1

    # バリア関連のプロパティ
    self.has_barrier = False

    self.barrier_effect_image = None
    self.barrier_effect_rect = None
    barrier_image_path = os.path.join('assets', 'images', 'items', 'item_barrier.png')
    if os.path.exists(barrier_image_path):
      original_barrier_image = pygame.image.load(barrier_image_path).convert_alpha()
      effect_size = int(self.rect.width * 1.5)
      self.barrier_effect_image = pygame.transform.scale(original_barrier_image, (effect_size, effect_size))
      self.barrier_effect_image.set_alpha(200)
      
      # 初期位置をプレイヤーの中心に設定
      self.barrier_effect_rect = self.barrier_effect_image.get_rect()
      self.barrier_effect_rect.center = self.rect.center
    else:
      print(f"バリアエフェクト画像がないよ: {barrier_image_path}")

  def update(self, keys):
    if self.hp <= 0:
      return
    
    current_time = pygame.time.get_ticks()
    
    # 減速効果タイマー処理
    if self.is_slowed:
      current_time = pygame.time.get_ticks()
      if current_time - self.slow_start_time > self.slow_duration:
        self.is_slowed = False
        print(f"プレイヤー{self.player_id}の減速効果が終了しました。")

    # 点滅処理
    if current_time - self.last_hit_time < self.invicibility_duration:
      self.is_invincible_blinking = True
      if current_time - self.last_blink_time > self.blink_interval:
        self.is_visible = not self.is_visible
        self.last_blink_time = current_time
        self.image = self.original_image if self.is_visible else pygame.Surface([self.rect.width, self.rect.height], pygame.SRCALPHA)
    else:
      self.is_invincible_blinking = False
      self.is_visible = True
      self.image = self.original_image

    # 移動速度計算
    current_speed = self.speed * self.slow_factor if self.is_slowed else self.speed

    if keys[self.keys_left]:
      self.rect.x -= current_speed
    if keys[self.keys_right]:
      self.rect.x += current_speed
    if keys[self.keys_up]:
      self.rect.y -= current_speed
    if keys[self.keys_down]:
      self.rect.y += current_speed

    # 画面の端で停止
    if self.rect.left < 0:
        self.rect.left = 0
    if self.rect.right > self.screen_width:
        self.rect.right = self.screen_width
    if self.rect.top < 0:
        self.rect.top = 0
    if self.rect.bottom > self.screen_height:
        self.rect.bottom = self.screen_height

    self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
    self.rect.y = max(self.min_y, min(self.rect.y, self.max_y))

    # バリアエフェクト
    if self.has_barrier and self.barrier_effect_rect:
      self.barrier_effect_rect.center = self.rect.center

  def shoot(self):
    if self.hp <= 0:
      return None
    
    current_time = pygame.time.get_ticks()
    if current_time - self.last_shot_time > self.shoot_delay:
      self.last_shot_time = current_time
      if self.shot_sound:
        self.shot_sound.play()
      
      # パワーショット(アイテム)が有効な場合は倍率を適用
      damage = 1
      if self.is_power_shot_active:
        elapsed = current_time - self.is_power_shot_start_time
        if elapsed < self.power_shot_duration:
          damage = self.current_damage_multiplier
        else:
          self.is_power_shot_active = False
          self.current_damage_multiplier = 1

      return Shot(self.rect.centerx, self.rect.top, self.color, owner_player=self, damage=damage)
    return None
  
  def take_damage(self, damage_amount=1):
    current_time = pygame.time.get_ticks()
    if current_time - self.last_hit_time > self.invicibility_duration:
      if self.has_barrier:
        self.has_barrier = False
        print(f"プレイヤー{self.player_id}のバリアがダメージを防ぎました！")
        return False
      else:
        self.hp -= damage_amount
        self.last_hit_time = current_time
        print(f"プレイヤー{self.player_id}がダメージを受けました！残りHP: {self.hp}")

        # プレイヤー被弾音の再生
        if self.hit_sound:
          self.hit_sound.play()

        if self.hp <= 0:
          self.kill()

        return True
    return False
  
  def add_score(self, value):
    self.score += value
    if self.score < 0:
      self.score = 0
  
  # プレイヤーを減速させるメソッド
  def apply_slow_effect(self):
    if not self.is_slowed:
      self.is_slowed = True
      self.slow_start_time = pygame.time.get_ticks()
      print(f"プレイヤー{self.color}が減速効果を受けました！")
  
  def is_alive(self):
    return self.hp > 0
  
  # パワーショット(アイテム)効果を適用するメソッド
  def apply_power_shot(self, multiplier, duration):
    self.is_power_shot_active = True
    self.is_power_shot_start_time = pygame.time.get_ticks()
    self.power_shot_duration = duration
    self.current_damage_multiplier = multiplier
    print(f"プレイヤー{self.player_id}にパワーショット効果が適用されました！")

  # バリア関連のメソッド
  def activate_barrier(self):
    self.has_barrier = True
    # バリアアクティベート時に確実に位置を更新
    if self.barrier_effect_rect:
      self.barrier_effect_rect.center = self.rect.center
    print(f"プレイヤー{self.player_id}にバリアを展開しました！")
  
  def has_active_barrier(self):
    return self.has_barrier
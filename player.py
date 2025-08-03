import pygame
import os
import math
from shots.shot import Shot
from shots.normal_shot import NormalShot
from shots.power_shot import PowerShot
from shots.triple_shot import TripleShot
from shots.piercing_shot import PiercingShot

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, color, keys_left, keys_right, keys_up, keys_down, speed, screen_width, screen_height, player_id, size=70):
    super().__init__()

    self.player_size = size
    self.image = pygame.Surface([self.player_size, self.player_size])
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

    # 速度アップ関連のプロパティ
    self.is_speed_up_active = False
    self.speed_up_start_time = 0
    self.speed_up_duration = 0
    self.speed_up_multiplier = 1.0

    self.score = 0
    self.hp = 3
    self.max_hp = 3

    # 被弾後の無敵時間
    self.last_hit_time = 0
    self.invicibility_duration = 1500
    self.is_invincible_blinking = False
    self.blink_interval = 100
    self.last_blink_time = 0
    self.is_visible = True

    # アイテムによる無敵時間
    self.is_item_invincible_active = False
    self.item_invincibility_start_time = 0
    self.item_invincibility_duration = 0

    # 無敵エフェクト(色)
    self.color_change_timer = 0
    self.color_list = [
      (255, 0, 0),    # 赤
      (255, 127, 0),  # 橙
      (255, 255, 0),  # 黄
      (0, 255, 0),    # 緑
      (0, 0, 255),    # 青
      (75, 0, 130),   # 藍
      (143, 0, 255)   # 紫
    ]
    self.current_color_index = 0
    self.color_change_interval = 100

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

    # 画像のロード
    image_path = f"player{self.player_id}.png"
    full_path = os.path.join('assets', 'images', image_path)
    
    if os.path.exists(full_path):
      original_image = pygame.image.load(full_path).convert_alpha()
      # プレイヤーサイズに合わせてスケール
      self.original_image = pygame.transform.scale(original_image, (self.player_size, self.player_size))
      self.image = self.original_image.copy()
    else:
      print(f"プレイヤー画像が見つかりません: {full_path}")
      self.original_image = pygame.Surface([self.player_size, self.player_size])
      self.original_image.fill(color)
      self.image = self.original_image.copy()

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

    # バリア関連のプロパティ
    self.has_barrier = False

    self.barrier_effect_image = None
    self.barrier_effect_rect = None
    barrier_image_path = os.path.join('assets', 'images', 'items', 'item_barrier.png')
    if os.path.exists(barrier_image_path):
      original_barrier_image = pygame.image.load(barrier_image_path).convert_alpha()
      # プレイヤーサイズに比例してバリアサイズを調整
      effect_size = int(self.player_size * 1.1)
      self.barrier_effect_image = pygame.transform.scale(original_barrier_image, (effect_size, effect_size))
      self.barrier_effect_image.set_alpha(150)
      
      self.barrier_effect_rect = self.barrier_effect_image.get_rect()
      self.barrier_effect_rect.center = self.rect.center
    else:
      print(f"バリアエフェクト画像がないよ: {barrier_image_path}")

    # 三方向ショット関連のプロパティ
    self.is_triple_shot_active = False
    self.triple_shot_start_time = 0
    self.triple_shot_duration = 0
    self.triple_shot_angle_offset = 15

    # 貫通ショット関連のプロパティ
    self.is_piercing_shot_active = False
    self.piercing_shot_count = 0
    self.piercing_shot_max_uses = 3

    self.active_shot_type = "normal"

  def update(self, keys):
    if self.hp <= 0:
      return
    
    current_time = pygame.time.get_ticks()
    
    # 減速効果タイマー処理
    if self.is_slowed:
      current_time = pygame.time.get_ticks()
      if current_time - self.slow_start_time > self.slow_duration:
        self.is_slowed = False
        self.speed = self.original_speed
        print(f"プレイヤー{self.player_id}の減速効果が終了しました。")

    # パワーショットタイマー処理
    if self.is_power_shot_active:
      if current_time - self.power_shot_start_time > self.power_shot_duration:
        self.is_power_shot_active = False
        print(f"プレイヤー{self.player_id}のパワーショット効果が終了しました。")
        if not self.is_triple_shot_active and not self.is_piercing_shot_active:
          self.active_shot_type = "normal"

    # 三方向ショットタイマー処理
    if self.is_triple_shot_active:
      if current_time - self.triple_shot_start_time > self.triple_shot_duration:
        self.is_triple_shot_active = False
        print(f"プレイヤー{self.player_id}の三方向ショット効果が終了しました。")
        if not self.is_power_shot_active and not self.is_piercing_shot_active:
          self.active_shot_type = "normal"

    # 貫通ショットタイマー処理
    if self.is_piercing_shot_active and self.piercing_shot_count <= 0:
      self.is_piercing_shot_active = False
      if not self.is_power_shot_active and not self.is_triple_shot_active:
        self.active_shot_type = "normal"
    
    # 速度アップタイマー処理
    if self.is_speed_up_active:
      if current_time - self.speed_up_start_time > self.speed_up_duration:
        self.is_speed_up_active = False
        self.speed = self.original_speed

    # アイテムによる無敵時間タイマー処理
    if self.is_item_invincible_active:
      if current_time - self.item_invincibility_start_time > self.item_invincibility_duration:
        self.is_item_invincible_active = False
        print(f"プレイヤー{self.player_id}の無敵効果が終了しました。")
        self.image = self.original_image.copy()
      elif current_time - self.color_change_timer > self.color_change_interval:
        self.color_change_timer = current_time
        self.current_color_index = (self.current_color_index + 1) % len(self.color_list)
        new_color = self.color_list[self.current_color_index]
        self.image.fill(new_color)
    else:
      pass

    # 点滅処理
    is_temp_invincible = current_time - self.last_hit_time < self.invicibility_duration
    if is_temp_invincible and not self.is_item_invincible_active:
      self.is_invincible_blinking = True
      if current_time - self.last_blink_time > self.blink_interval:
        self.is_visible = not self.is_visible
        self.last_blink_time = current_time
    else:
      self.is_invincible_blinking = False
      self.is_visible = True

    # 移動速度計算
    current_speed = self.speed * self.slow_factor if self.is_slowed else self.speed
    if self.is_speed_up_active:
      current_speed *= self.speed_up_multiplier

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

    self.rect.x = max(0, min(self.rect.x, self.screen_width - self.player_size))
    self.rect.y = max(self.min_y, min(self.rect.y, self.screen_height - self.player_size))

    # バリアエフェクト
    if self.has_barrier and self.barrier_effect_rect:
      self.barrier_effect_rect.center = self.rect.center

  def shoot(self):
    if self.hp <= 0:
      return []
    
    current_time = pygame.time.get_ticks()
    if current_time - self.last_shot_time > self.shoot_delay:
      self.last_shot_time = current_time
      if self.shot_sound:
        self.shot_sound.play()
      
      shots_to_fire = []
      is_power_active = self.is_power_shot_active

      if self.active_shot_type == "triple":
        triple_shot_base_speed = -15
        angles_deg = [self.triple_shot_angle_offset, 0, -self.triple_shot_angle_offset]
        for angle_deg in angles_deg:
          angle_rad = math.radians(angle_deg)
          total_shot_speed = abs(triple_shot_base_speed)
          current_vy = -total_shot_speed * math.cos(angle_rad)
          current_vx = total_shot_speed * math.sin(angle_rad)
          offset_x, offset_y = (10, 5) if angle_deg > 0 else (-10, 5) if angle_deg < 0 else (0, 0)
          shots_to_fire.append(TripleShot(self.rect.centerx + offset_x, self.rect.top + offset_y, 
                                      owner_player=self, vx=current_vx, vy=current_vy,
                                      is_power_active=is_power_active))
      elif self.active_shot_type == "piercing" and self.piercing_shot_count > 0:
        shots_to_fire.append(PiercingShot(self.rect.centerx, self.rect.top, owner_player=self, is_power_active=is_power_active))
        self.piercing_shot_count -= 1
      elif self.active_shot_type == "power":
        shots_to_fire.append(PowerShot(self.rect.centerx, self.rect.top, owner_player=self, is_power_active=is_power_active))
      else:
        shots_to_fire.append(NormalShot(self.rect.centerx, self.rect.top, owner_player=self, is_power_active=is_power_active))
      
      return shots_to_fire
    return []
  
  def take_damage(self, damage_amount=1):
    current_time = pygame.time.get_ticks()

    if self.is_item_invincible_active:
      print(f"プレイヤー{self.player_id}は無敵効果によりダメージを防ぎました！")
      return False
    
    if current_time - self.last_hit_time < self.invicibility_duration:
        return False

    if self.has_barrier:
      self.has_barrier = False
      print(f"プレイヤー{self.player_id}のバリアがダメージを防ぎました！")
      return False
    
    self.hp -= damage_amount
    self.last_hit_time = current_time
    print(f"プレイヤー{self.player_id}がダメージを受けました！残りHP: {self.hp}")
    
    # プレイヤー被弾音の再生
    if self.hit_sound:
      self.hit_sound.play()

    if self.hp <= 0:
      self.kill()

    return True
  
  def add_score(self, value):
    self.score += value
    if self.score < 0:
      self.score = 0
  
  # プレイヤーを減速させるメソッド
  def apply_slow_effect(self, duration_ms=5000):
    if not self.is_slowed:
      self.is_slowed = True
      self.slow_start_time = pygame.time.get_ticks()
      self.slow_duration = duration_ms
      print(f"プレイヤー{self.player_id}が減速効果を受けました！")
  
  def is_alive(self):
    return self.hp > 0
  
  # パワーショット(アイテム)効果を適用するメソッド
  def apply_power_shot(self, multiplier, duration):
    self.deactivate_all_shot_effects()

    self.is_power_shot_active = True
    self.power_shot_start_time = pygame.time.get_ticks()
    self.power_shot_duration = duration
    self.current_damage_multiplier = multiplier
    self.active_shot_type = "power"
    print(f"プレイヤー{self.player_id}にパワーショット効果が適用されました！")

  # バリア関連のメソッド
  def activate_barrier(self):
    self.has_barrier = True
    if self.barrier_effect_rect:
      self.barrier_effect_rect.center = self.rect.center
    print(f"プレイヤー{self.player_id}にバリアを展開しました！")
  
  def has_active_barrier(self):
    return self.has_barrier
  
  # 三方向ショットをアクティブにするメソッド
  def activate_triple_shot(self, duration_ms):
    self.deactivate_all_shot_effects()

    self.is_triple_shot_active = True
    self.triple_shot_start_time = pygame.time.get_ticks()
    self.triple_shot_duration = duration_ms
    self.active_shot_type = "triple"
    print(f"プレイヤー{self.player_id}に三方向ショット効果が適用されました！")

  # ショット効果を全て無効化するヘルパーメソッド
  def deactivate_all_shot_effects(self):
    self.is_power_shot_active = False
    self.is_triple_shot_active = False
    self.is_piercing_shot_active = False
    self.active_shot_type = "normal"

  # 貫通ショットをアクティブにするメソッド
  def activate_piercing_shot(self, num_uses):
    self.deactivate_all_shot_effects()
    self.is_piercing_shot_active = True
    self.piercing_shot_count = num_uses
    self.active_shot_type = "piercing"
    print(f"プレイヤー{self.player_id}に貫通ショット効果が適用されました！残り {self.piercing_shot_count} 発")

  # 無敵をアクティブにするメソッド
  def activate_invincibility(self, duration_ms):
    self.is_item_invincible_active = True
    self.item_invincibility_start_time = pygame.time.get_ticks()
    self.item_invincibility_duration = duration_ms
    print(f"プレイヤー{self.player_id}が無敵になりました！")

  def has_active_triple_shot(self):
    return self.is_triple_shot_active
  
  def activate_speed_up(self, duration_ms, multiplier):
    self.is_speed_up_active = True
    self.speed_up_start_time = pygame.time.get_ticks()
    self.speed_up_duration = duration_ms
    self.speed_up_multiplier = multiplier
    print(f"プレイヤー{self.player_id}の移動速度が {multiplier} 倍になりました！")
    
  def has_active_speed_up(self):
    return self.is_speed_up_active
  
  def draw(self, screen):
    is_temp_invincible = pygame.time.get_ticks() - self.last_hit_time < self.invicibility_duration
    is_currently_visible = self.is_visible or self.is_item_invincible_active

    if is_currently_visible:
      current_image = self.original_image.copy()

      if self.is_item_invincible_active:
        rainbow_color = self.color_list[self.current_color_index]
        color_image = pygame.Surface(current_image.get_size()).convert_alpha()
        color_image.fill(rainbow_color)
        current_image.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
      screen.blit(current_image, self.rect)
  
    # バリアエフェクトの描画
    if self.has_barrier and self.barrier_effect_image:
      self.barrier_effect_rect.center = self.rect.center
      screen.blit(self.barrier_effect_image, self.barrier_effect_rect)
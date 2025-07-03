import pygame
from shot import Shot
import os

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, color, keys_left, keys_right, keys_up, keys_down, speed, screen_width, screen_height):
    super().__init__()

    self.image = pygame.Surface([50, 50])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

    self.color = color
    self.speed = speed

    self.score = 0
    self.hp = 3
    self.last_hit_time = 0
    self.invicibility_duration = 2000

    self.keys_left = keys_left
    self.keys_right = keys_right
    self.keys_up = keys_up
    self.keys_down = keys_down

    self.screen_width = screen_width
    self.screen_height = screen_height

    self.min_y = self.screen_height // 2
    self.max_y = self.screen_height - self.rect.height

    # 効果音のロード
    self.shot_sound = None
    self.hit_sound = None
    shot_sound_path = os.path.join('assets', 'sounds', 'shot.mp3')
    player_hit_sound_path = os.path.join('assets', 'sounds', 'player_hit.mp3')
    if os.path.exists(shot_sound_path):
      self.shot_sound = pygame.mixer.Sound(shot_sound_path)
      self.shot_sound.set_volume(0.2)
    else:
      print(f"Warning: Shot sound file not found at {shot_sound_path}")
    if os.path.exists(player_hit_sound_path):
      self.hit_sound = pygame.mixer.Sound(player_hit_sound_path)
      self.hit_sound.set_volume(0.2)
    else:
      print(f"効果音がないよ: {player_hit_sound_path}")


  def update(self, keys):
    if self.hp <= 0:
      return

    if keys[self.keys_left]:
      self.rect.x -= self.speed
    if keys[self.keys_right]:
      self.rect.x += self.speed
    if keys[self.keys_up]:
      self.rect.y -= self.speed
    if keys[self.keys_down]:
      self.rect.y += self.speed

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

  def shoot(self):
    if self.hp <= 0:
      return None

    # ショット音の再生
    if self.shot_sound:
      self.shot_sound.play()

    new_shot = Shot(self.rect.centerx, self.rect.top, self.color)
    new_shot.owner_player = self
    return new_shot
  
  def take_damage(self):
    current_time = pygame.time.get_ticks()
    if current_time - self.last_hit_time > self.invicibility_duration:
      self.hp -= 1
      self.last_hit_time = current_time
      print(f"プレイヤー{self.color}がダメージを受けました！残りHP: {self.hp}")

      # プレイヤー被弾音の再生
      if self.hit_sound:
        self.hit_sound.play()

      return True
    return False
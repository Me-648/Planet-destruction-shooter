# 抽象基底クラス
import pygame
import os

class GameState:
  def __init__(self, screen, font, small_font, game_manager):
    self.screen = screen
    self.font = font
    self.small_font = small_font
    self.game_manager = game_manager
    self.screen_width, self.screen_height = self.screen.get_size()

    # 背景に関するプロパティ
    self.background_image_original = None
    self.background_image_scaled = None

    self.background_y1 = 0
    self.background_y2 = 0
    self.background_speed = 0.5

    self.static_background_image = None
    self.static_background_rect = None

  def load_scrolling_background(self, image_path, speed=0.5):
    if image_path and os.path.exists(image_path):
      self.background_image_original = pygame.image.load(image_path).convert()
      original_width, original_height = self.background_image_original.get_size()
      aspect_ratio = original_height / original_width

      new_height = int(self.screen_width * aspect_ratio)

      self.background_image_scaled = pygame.transform.scale(
        self.background_image_original,
        (self.screen_width, new_height)
      )

      self.background_y1 = 0
      self.background_y2 = -new_height
      self.background_speed = speed
    else:
      print(f"背景がないよー: {image_path}. デフォルトの使うねー")
      self.background_image_original = None
      self.background_image_scaled = None

  def load_static_background_cover(self, image_path):
    if image_path and os.path.exists(image_path):
      original_image = pygame.image.load(image_path).convert()
      original_width, original_height = original_image.get_size()

      screen_aspect_ratio = self.screen_width / self.screen_height
      image_aspect_ratio = original_width / original_height

      if screen_aspect_ratio > image_aspect_ratio:
              # 画面が画像より横長の場合、幅に合わせて拡大し、高さははみ出る
              new_width = self.screen_width
              new_height = int(self.screen_width / image_aspect_ratio)
      else:
              # 画面が画像より縦長の場合、高さに合わせて拡大し、幅ははみ出る
              new_height = self.screen_height
              new_width = int(self.screen_height * image_aspect_ratio)
          
      self.static_background_image = pygame.transform.scale(original_image, (new_width, new_height))
          
          # 画面中央に配置するため、左上の座標を計算
      x_offset = (self.screen_width - new_width) // 2
      y_offset = (self.screen_height - new_height) // 2
      self.static_background_rect = self.static_background_image.get_rect(topleft=(x_offset, y_offset))
    else:
          print(f"Warning: Static background image not found at {image_path}. Using default gray background.")
          self.static_background_image = None
          self.static_background_rect = None
  
  def draw_static_background(self):
      self.screen.fill((0, 0, 0)) # まず画面全体を黒で塗りつぶす (はみ出た部分が黒になる)
      if self.static_background_image and self.static_background_rect:
          self.screen.blit(self.static_background_image, self.static_background_rect)
      else:
          self.screen.fill((128, 128, 128))


  def update_background(self):
    self.background_y1 += self.background_speed
    self.background_y2 += self.background_speed

    image_height = self.background_image_scaled.get_height()
    if self.background_y1 >= image_height:
      self.background_y1 = -image_height
    if self.background_y2 >= image_height:
      self.background_y2 = -image_height
  
  def draw_background(self):
    self.screen.fill((128, 128, 128))

    if self.background_image_scaled:
      self.screen.blit(self.background_image_scaled, (0, self.background_y1))
      self.screen.blit(self.background_image_scaled, (0, self.background_y2))
    else:
      self.screen.fill((128, 128, 128))

  def handle_event(self, event):
    pass
  
  def update(self):
    pass
  
  def draw(self):
    pass
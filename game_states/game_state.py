# 抽象基底クラス
import pygame

class GameState:
  def __init__(self, screen, font, small_font, game_manager):
    self.screen = screen
    self.font = font
    self.small_font = small_font
    self.game_manager = game_manager

  def handle_event(self, event):
    # イベント処理を行う中小メソッド
    raise NotImplementedError
  
  def update(self):
    # 状態更新を行う抽象メソッド
    raise NotImplementedError
  
  def draw(self):
    # 描画を行う抽象メソッド
    raise NotImplementedError
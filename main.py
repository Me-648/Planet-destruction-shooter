import pygame
import sys

from game_states.title_screen import TitleScreen
from game_states.game_screen import GameScreen
from game_states.how_to_play_screen import HowToPlayScreen

# 初期設定
pygame.init()

# 画面サイズ
# 初期解像度
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
# フルスクリーンに設定
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

pygame.display.set_caption("惑星破壊シューティングII (準備中)")

# ゲーム状態の定数定義
GAME_STATE_TITLE = "title"    # タイトル画面
GAME_STATE_PLAYING = "playing"  #ゲームプレイ中
GAME_STATE_HOW_TO_PLAY = "how_to_play"  # 遊び方説明画面

class GameManager:
  def __init__(self):
    self.screen = screen
    self.screen_width, self.screen_height = self.screen.get_size()

    # フォント設定
    try:
      self.font = pygame.font.Font("WDXLLubrifontSC-Regular.ttf", 74)
      self.small_font = pygame.font.Font("WDXLLubrifontSC-Regular.ttf", 48)
    except FileNotFoundError:
      print("指定されたフォントファイルが見つかりません。デフォルトフォントを使用します")
      self.font = pygame.font.Font(None, 74)
      self.small_font = pygame.font.Font(None, 48)

    # 各ゲーム状態のインスタンス
    self.title_screen = TitleScreen(self.screen, self.font, self.small_font, self)
    self.game_screen = GameScreen(self.screen, self.font, self.small_font, self)
    self.how_to_play_screen = HowToPlayScreen(self.screen, self.font, self.small_font, self)
    self.states = {
      GAME_STATE_TITLE: self.title_screen,
      GAME_STATE_PLAYING: self.game_screen,
      GAME_STATE_HOW_TO_PLAY: self.how_to_play_screen
    }
    self.current_state = self.states[GAME_STATE_TITLE]

  def change_state(self, new_state_name):
    if new_state_name in self.states:
      if new_state_name == GAME_STATE_PLAYING:
        self.game_screen.reset_game()
      self.current_state = self.states[new_state_name]
      print(f"ゲーム状態が {new_state_name} に変更されました。")
    else:
      print(f"エラー: 未知のゲーム状態'{new_state_name}'")

  def run(self):
    clock = pygame.time.Clock()
    FPS = 60
    running = True

    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
        self.current_state.handle_event(event)

      self.current_state.update()
      self.current_state.draw()
      pygame.display.flip()
      clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
  game_manager = GameManager()
  game_manager.run()
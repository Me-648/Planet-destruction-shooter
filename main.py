import pygame
import sys
import os

from game_states.title_screen import TitleScreen
from game_states.game_screen import GameScreen
from game_states.how_to_play_screen import HowToPlayScreen
from game_states.game_over_screen import GameOverScreen

# 初期設定
pygame.init()
pygame.mixer.init()

# 画面サイズ
# 初期解像度
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("惑星破壊シューティングII (準備中)")

# ゲーム状態の定数定義
GAME_STATE_TITLE = "title"    # タイトル画面
GAME_STATE_PLAYING = "playing"  #ゲームプレイ中
GAME_STATE_HOW_TO_PLAY = "how_to_play"  # 遊び方説明画面
GAME_STATE_GAME_OVER = "game_over" #ゲームオーバー画面

class GameManager:
  def __init__(self):
    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    self.screen_width, self.screen_height = self.screen.get_size()

    # フォント設定
    try:
      self.font = pygame.font.Font("WDXLLubrifontSC-Regular.ttf", 74)
      self.small_font = pygame.font.Font("WDXLLubrifontSC-Regular.ttf", 48)
    except FileNotFoundError:
      print("指定されたフォントファイルが見つかりません。デフォルトフォントを使用します")
      self.font = pygame.font.Font(None, 74)
      self.small_font = pygame.font.Font(None, 48)

    # BGMのロード
    self.bgm_paths = {
      GAME_STATE_TITLE: os.path.join('assets', 'sounds', 'title_bgm.mp3'), # タイトルBGM
      GAME_STATE_PLAYING: os.path.join('assets', 'sounds', 'game_bgm.mp3'), # ゲームプレイBGM
      GAME_STATE_HOW_TO_PLAY: os.path.join('assets', 'sounds', 'title_bgm.mp3'),  # 遊び方画面(titleと同じ)
      GAME_STATE_GAME_OVER: os.path.join('assets', 'sounds', 'game_over_bgm.mp3'), # ゲームオーバーBGM
    }
    # 各BGMの音量
    self.bgm_volumes = {
      GAME_STATE_TITLE: 1.0,
      GAME_STATE_PLAYING: 0.1,
      GAME_STATE_HOW_TO_PLAY: 1.0,
      GAME_STATE_GAME_OVER: 0.3,
    }

    self.current_bgm_path = None

    # 各ゲーム状態のインスタンス
    self.title_screen = TitleScreen(self.screen, self.font, self.small_font, self)
    self.game_screen = GameScreen(self.screen, self.font, self.small_font, self)
    self.how_to_play_screen = HowToPlayScreen(self.screen, self.font, self.small_font, self)
    self.game_over_screen = GameOverScreen(self.screen, self.font, self.small_font, self)
    self.states = {
      GAME_STATE_TITLE: self.title_screen,
      GAME_STATE_PLAYING: self.game_screen,
      GAME_STATE_HOW_TO_PLAY: self.how_to_play_screen,
      GAME_STATE_GAME_OVER: self.game_over_screen,
    }
    self.current_state = self.states[GAME_STATE_TITLE]

  def change_state(self, new_state_name, p1_score=0, p2_score=0):
    if new_state_name in self.states:
      new_bgm_path = self.bgm_paths.get(new_state_name)

      should_change_bgm = False

      # 現在BGMが再生されていない場合、またはBGMパスが存在しない場合は、常に切り替える
      if not pygame.mixer.music.get_busy() or new_bgm_path is None:
        should_change_bgm = True
      # 新しいBGMパスが現在のBGMパスと異なる場合 (つまり、別のBGMに切り替わる場合)
      elif new_bgm_path != self.current_bgm_path:
        should_change_bgm = True
      # 新しい状態がゲームオーバー画面の場合 (1回再生のため、常に切り替え)
      elif new_state_name == GAME_STATE_GAME_OVER:
        should_change_bgm = True

      if should_change_bgm:
        pygame.mixer.music.stop()
        self.current_bgm_path = None

        if new_bgm_path and os.path.exists(new_bgm_path):
          pygame.mixer.music.load(new_bgm_path)
          volume = self.bgm_volumes.get(new_state_name, 1.0)
          pygame.mixer.music.set_volume(volume)

          if new_state_name == GAME_STATE_GAME_OVER:
            pygame.mixer.music.play(0)
          else:
            pygame.mixer.music.play(-1)
          self.current_bgm_path = new_bgm_path
        else:
          print(f"bgmない {new_state_name} / {new_bgm_path}")
      
      self.current_state_name = new_state_name

      if new_state_name == GAME_STATE_PLAYING:
        self.game_screen.reset_game()
      elif new_state_name == GAME_STATE_GAME_OVER:
        self.game_over_screen.set_final_scores(p1_score, p2_score)
      self.current_state = self.states[new_state_name]
      print(f"ゲーム状態が {new_state_name} に変更されました。")
    else:
      print(f"エラー: 未知のゲーム状態'{new_state_name}'")

  def run(self):
    # タイトル画面のBGMを作成
    self.change_state(GAME_STATE_TITLE)

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
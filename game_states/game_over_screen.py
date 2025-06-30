import pygame
from game_states.game_state import GameState

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

class GameOverScreen(GameState):
  def __init__(self, screen, font, small_font, game_manager):
    super().__init__(screen, font, small_font, game_manager)
    self.screen_width, self.screen_height = self.screen.get_size()

    # ボタンの短形を定義(サイズを大きめに)
    button_width = 280
    button_height = 60

    # 最終スコア表示用
    self.player1_final_score = 0
    self.player2_final_score = 0

    self.restart_button_rect = pygame.Rect(0, 0, button_width, button_height)
    self.title_button_rect = pygame.Rect(0, 0, button_width, button_height)
    self.exit_button_rect = pygame.Rect(0, 0, button_width, button_height)

  # ゲームオーバー画面遷移メソッド
  def set_final_scores(self, p1_score, p2_score):
    self.player1_final_score = p1_score
    self.player2_final_score = p2_score

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = event.pos
      if self.restart_button_rect.collidepoint(mouse_pos):
        # ゲームプレイ画面に遷移(ゲームをリセット)
        self.game_manager.change_state("playing")
      elif self.title_button_rect.collidepoint(mouse_pos):
        # タイトル画面に遷移
        self.game_manager.change_state("title")
      elif self.exit_button_rect.collidepoint(mouse_pos):
        # ゲームを終了
        pygame.quit()
        import sys
        sys.exit()

  def update(self):
    pass

  def draw(self):
    self.screen.fill(GRAY)

    # ゲームオーバータイトル
    game_over_text = self.font.render("★全滅しました★", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
    self.screen.blit(game_over_text, game_over_rect)

    # 最終スコア表示
    p1_final_score_text = self.small_font.render(f"プレイヤー1 スコア: {self.player1_final_score}", True, BLUE)
    p1_final_score_rect = p1_final_score_text.get_rect(center=(self.screen_width // 2, game_over_rect.bottom + 50))
    self.screen.blit(p1_final_score_text, p1_final_score_rect)

    p2_final_score_text = self.small_font.render(f"プレイヤー2 スコア: {self.player2_final_score}", True, (0, 255, 0)) # 緑色
    p2_final_score_rect = p2_final_score_text.get_rect(center=(self.screen_width // 2, p1_final_score_rect.bottom + 40))
    self.screen.blit(p2_final_score_text, p2_final_score_rect)

    # 勝者を表示
    winner_message = ""
    if self.player1_final_score > self.player2_final_score:
      winner_message = "プレイヤー1の勝ち！"
    elif self.player2_final_score > self.player1_final_score:
      winner_message = "プレイヤー2の勝ち！"
    else:
      winner_message = "引き分け"

    winner_text_surface = self.small_font.render(winner_message, True, WHITE)
    winner_text_rect = winner_text_surface.get_rect(center=(self.screen_width // 2, p2_final_score_rect.bottom + 60))
    self.screen.blit(winner_text_surface, winner_text_rect)


    # ボタン描画
    # リスタートボタン
    self.restart_button_rect.center = (self.screen_width // 2, winner_text_rect.bottom + 100)
    pygame.draw.rect(self.screen, BLUE, self.restart_button_rect)
    restart_text = self.small_font.render("もう一度play", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
    self.screen.blit(restart_text, restart_text_rect)

    # タイトルへ戻るボタン
    self.title_button_rect.center = (self.screen_width // 2, self.restart_button_rect.bottom + 50)
    pygame.draw.rect(self.screen, (255, 165, 0), self.title_button_rect)
    title_text = self.small_font.render("タイトルへ", True, WHITE)
    title_text_rect = title_text.get_rect(center=self.title_button_rect.center)
    self.screen.blit(title_text, title_text_rect)

    # 終了ボタン
    self.exit_button_rect.center = (self.screen_width // 2, self.title_button_rect.bottom + 50)
    pygame.draw.rect(self.screen, (200, 0, 0), self.exit_button_rect)
    exit_text = self.small_font.render("終了", True, WHITE)
    exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
    self.screen.blit(exit_text, exit_text_rect)

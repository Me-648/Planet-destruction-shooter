import pygame
from game_states.game_state import GameState

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

class TitleScreen(GameState):
  def __init__(self, screen, font, small_font, game_manager):
    super().__init__(screen, font, small_font, game_manager)
    self.screen_width, self.screen_height = self.screen.get_size()
    self.play_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2, 200, 50)
    self.how_to_play_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 70, 200, 50)

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        mouse_pos = event.pos
        if self.play_button_rect.collidepoint(mouse_pos):
          self.game_manager.change_state("playing") # GameManagerに状態変更を依頼
        elif self.how_to_play_button_rect.collidepoint(mouse_pos):
          self.game_manager.change_state("how_to_play") # GameManagerに状態変更を依頼

  def update(self):
    pass

  def draw(self):
    self.screen.fill(GRAY)
    # タイトルテキスト
    title_text = self.font.render("惑星破壊シューティングⅡ", True, WHITE)
    title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
    self.screen.blit(title_text, title_rect)

    # Playボタンの描画
    pygame.draw.rect(self.screen, BLUE, self.play_button_rect)
    play_text = self.small_font.render("PLAY", True, WHITE)
    play_text_rect = play_text.get_rect(center=self.play_button_rect.center)
    self.screen.blit(play_text, play_text_rect)

    # 遊び方ボタンの描画
    pygame.draw.rect(self.screen, ORANGE, self.how_to_play_button_rect)
    how_to_play_text = self.small_font.render("遊び方", True, WHITE)
    how_to_play_text_rect = how_to_play_text.get_rect(center=self.how_to_play_button_rect.center)
    self.screen.blit(how_to_play_text, how_to_play_text_rect)
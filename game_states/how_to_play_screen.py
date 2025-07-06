import pygame
from game_states.game_state import GameState

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

class HowToPlayScreen(GameState):
  def __init__(self, screen, font, small_font, game_manager):
    super().__init__(screen, font, small_font, game_manager)
    self.screen_width, self.screen_height = self.screen.get_size()
    self.back_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height - 100, 200, 50)

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        mouse_pos = event.pos
        if self.back_button_rect.collidepoint(mouse_pos):
          self.game_manager.change_state("title") # GameManagerに状態変更を依頼
        
  def update(self):
    pass

  def draw(self):
    self.screen.fill(GRAY)

    # 遊び方説明画面の描画
    how_to_play_title_text = self.font.render("遊び方", True, WHITE)
    how_to_play_title_rect = how_to_play_title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
    self.screen.blit(how_to_play_title_text, how_to_play_title_rect)

    instructions_text_lines = [
      "プレイヤー1: A/D/W/Sキーで移動, SPACEキーでショット",
      "プレイヤー2: 矢印キーで移動, ENTERキーでショット",
      "宙から降ってくる惑星を破壊しましょう！",
      "様々な惑星が登場します！がんばって！！"
    ]
        
    y_offset = how_to_play_title_rect.bottom + 50
    for line in instructions_text_lines:
      instruction_text = self.small_font.render(line, True, WHITE)
      instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, y_offset))
      self.screen.blit(instruction_text, instruction_rect)
      y_offset += 70 # 行間

    # Backボタンの描画
    pygame.draw.rect(self.screen, BLUE, self.back_button_rect)
    back_text = self.small_font.render("戻る", True, WHITE)
    back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
    self.screen.blit(back_text, back_text_rect)
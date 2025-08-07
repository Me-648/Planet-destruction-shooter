import pygame
import os
from game_states.game_state import GameState

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

class HowToPlayScreen(GameState):
  def __init__(self, screen, font, small_font, game_manager):
    super().__init__(screen, font, small_font, game_manager)
    self.screen_width, self.screen_height = self.screen.get_size()
        
    # ページ管理
    self.current_page = 0
    self.total_pages = 6
    self.page_data = self.create_page_data()

    # ボタンの rect を設定
    self.back_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height - 100, 200, 50)
    self.prev_button_rect = pygame.Rect(self.back_button_rect.left - 70, self.back_button_rect.top, 50, 50)
    self.next_button_rect = pygame.Rect(self.back_button_rect.right + 20, self.back_button_rect.top, 50, 50)

    # 背景画像をロード
    background_path = os.path.join('assets', 'images', 'background.png')
    self.load_scrolling_background(background_path, speed=0.2)

    # 惑星とアイテムの画像を事前にロード
    self.load_images(self.page_data[1]["content"], os.path.join('assets', 'images', 'planets'))
    self.load_images(self.page_data[2]["content"], os.path.join('assets', 'images', 'planets'))
    self.load_images(self.page_data[3]["content"], os.path.join('assets', 'images', 'items'))
    self.load_images(self.page_data[4]["content"], os.path.join('assets', 'images', 'items'))
    self.load_images(self.page_data[5]["content"], os.path.join('assets', 'images', 'items'))

  # 表示するページの内容を定義するメソッド
  def create_page_data(self):
    # 惑星とアイテムの情報リスト
    planet_info = [
      {"name": "惑星", "image": "planet_normal.png", "description": "普通の惑星。"},
      {"name": "岩石惑星", "image": "planet_rock.png", "description": "破壊すると破片が飛ぶ。"},
      {"name": "中惑星", "image": "planet_mid.png", "description": "少し耐久力が高い"},
      {"name": "氷惑星", "image": "planet_ice.png", "description": "破壊したプレイヤーは一定時間減速する。"},
      {"name": "ウイルス惑星", "image": "planet_virus.png", "description": "破壊するとダメージを受ける"},
      {"name": "UFO", "image": "planet_ufo.png", "description": "近くにいるプレイヤーを攻撃してくる。"},
      {"name": "惑星...？", "image": "planet_penalty_1.png", "description": "破壊するとスコアが減少する。"},
    ]
    item_info = [
      {"name": "スコアコイン", "image": "item_score.png", "description": "スコアが加算される。"},
      {"name": "回復アイテム", "image": "item_heal.png", "description": "HPが2回復する。"},
      {"name": "スピードUP", "image": "item_speed_up.png", "description": "一定時間、プレイヤーの移動速度が上がる。"},
      {"name": "パワーショット", "image": "item_powershot.png", "description": "一定時間、弾の威力が5倍になる。"},
      {"name": "三方向ショット", "image": "item_triple_shot.png", "description": "一定時間、3方向に弾を発射する。"},
      {"name": "貫通ショット", "image": "item_piercing_shot.png", "description": "3発、惑星を貫通するショットが打てる。"},
      {"name": "バリア", "image": "item_barrier.png", "description": "攻撃を1度防ぐバリアを展開。"},
      {"name": "スロー", "image": "item_slow.png", "description": "一定時間、惑星の動きが遅くなる。"},
      {"name": "レインボースター", "image": "item_invincibility.png", "description": "一定時間、ダメージを受けない。"},
    ]

    # アイテムを3ページに分割
    items_per_page = 3
    item_info_page1 = item_info[:items_per_page]
    item_info_page2 = item_info[items_per_page:items_per_page*2]
    item_info_page3 = item_info[items_per_page*2:]

    return [
      {"title": "遊び方", "type": "instructions", "content": [
        "プレイヤー1: A/D/W/Sキーで移動, SPACEキーでショット",
        "プレイヤー2: 矢印キーで移動, ENTERキーでショット",
        "Pキーで一時停止/再開",
        "宙から降ってくる惑星を破壊しましょう！",
      ]},
      {"title": "惑星の種類 (1/2)", "type": "info", "content": planet_info[:4]},
      {"title": "惑星の種類 (2/2)", "type": "info", "content": planet_info[4:]},
      {"title": "アイテム (1/3)", "type": "info", "content": item_info_page1},
      {"title": "アイテム (2/3)", "type": "info", "content": item_info_page2},
      {"title": "アイテム (3/3)", "type": "info", "content": item_info_page3},
    ]

  def load_images(self, info_list, base_path):
    for item in info_list:
      image_path = os.path.join(base_path, item["image"])
      if os.path.exists(image_path):
        original_image = pygame.image.load(image_path).convert_alpha()
        item["loaded_image"] = pygame.transform.scale(original_image, (60, 60))
      else:
        print(f"Warning: Image not found at {image_path}")
        item["loaded_image"] = pygame.Surface((60, 60))
        item["loaded_image"].fill((255, 0, 255))

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        mouse_pos = event.pos
        if self.back_button_rect.collidepoint(mouse_pos):
          self.game_manager.change_state("title")
        elif self.next_button_rect.collidepoint(mouse_pos):
          self.current_page = (self.current_page + 1) % self.total_pages
        elif self.prev_button_rect.collidepoint(mouse_pos):
          self.current_page = (self.current_page - 1 + self.total_pages) % self.total_pages

  def update(self):
    self.update_background()

  def draw(self):
    self.draw_background()

    current_page_data = self.page_data[self.current_page]

    if current_page_data["type"] == "instructions":
      self.draw_instructions_page(current_page_data)
    elif current_page_data["type"] == "info":
      self.draw_info_page(current_page_data)

    self.draw_buttons()

  # 遊び方のページを描画するメソッド
  def draw_instructions_page(self, page_data):
    how_to_play_title_text = self.font.render(page_data["title"], True, WHITE)
    how_to_play_title_rect = how_to_play_title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
    self.screen.blit(how_to_play_title_text, how_to_play_title_rect)

    y_offset = how_to_play_title_rect.bottom + 50
    for line in page_data["content"]:
      instruction_text = self.small_font.render(line, True, WHITE)
      instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, y_offset))
      self.screen.blit(instruction_text, instruction_rect)
      y_offset += 70

  # 惑星/アイテム紹介のページを描画するメソッド
  def draw_info_page(self, page_data):
    start_y = self.screen_height // 4

    section_title_text = self.font.render(page_data["title"], True, WHITE)
    section_title_rect = section_title_text.get_rect(center=(self.screen_width // 2, start_y))
    self.screen.blit(section_title_text, section_title_rect)

    y_offset = section_title_rect.bottom + 50
    for item in page_data["content"]:
      if "loaded_image" in item:
        image_rect = item["loaded_image"].get_rect(topleft=(self.screen_width // 4, y_offset))
        self.screen.blit(item["loaded_image"], image_rect)
                
      # テキストを画像右側に配置
      text_x = self.screen_width // 4 + 80
      text_y = y_offset + 5
            
      # 説明文が長い場合は自動で折り返す
      max_text_width = self.screen_width - text_x - 40
      text_lines = self.wrap_text(f"{item['name']}: {item['description']}", self.small_font, max_text_width)

      for line in text_lines:
        text_surface = self.small_font.render(line, True, WHITE)
        self.screen.blit(text_surface, (text_x, text_y))
        text_y += text_surface.get_height() + 5

      y_offset += 70

  def wrap_text(self, text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
      test_line = ' '.join(current_line + [word])
      if font.size(test_line)[0] < max_width:
        current_line.append(word)
      else:
        lines.append(' '.join(current_line))
        current_line = [word]
    if current_line:
      lines.append(' '.join(current_line))
    return lines

  # 戻る、次へ、前へボタンを描画するメソッド
  def draw_buttons(self):
    pygame.draw.rect(self.screen, BLUE, self.back_button_rect)
    back_text = self.small_font.render("戻る", True, WHITE)
    back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
    self.screen.blit(back_text, back_text_rect)

    pygame.draw.rect(self.screen, BLUE, self.prev_button_rect)
    prev_text = self.font.render("←", True, WHITE)
    prev_text_rect = prev_text.get_rect(center=self.prev_button_rect.center)
    self.screen.blit(prev_text, prev_text_rect)

    pygame.draw.rect(self.screen, BLUE, self.next_button_rect)
    next_text = self.font.render("→", True, WHITE)
    next_text_rect = next_text.get_rect(center=self.next_button_rect.center)
    self.screen.blit(next_text, next_text_rect)
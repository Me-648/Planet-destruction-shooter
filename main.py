# main.py
import pygame
import sys
import random

from player import Player
from planets.normal_planet import NormalPlanet
from planets.rock_planet import RockPlanet

# --- 初期設定 ---
pygame.init()

# 画面サイズ
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("惑星破壊シューティングII (準備中)")

# 色の定義 (ここではゲーム全体で使う色を定義)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# ゲーム状態の定数定義
GAME_STATE_TITLE = 0    # タイトル画面
GAME_STATE_PLAYING = 1  #ゲームプレイ中
GAME_STATE_HOW_TO_PLAY = 2  # 遊び方説明画面

def main():
    # ゲームの現在の状態
    current_game_state = GAME_STATE_TITLE

    # フォント設定
    try:
        font = pygame.font.Font("WDXLLubrifontSC-Regular.ttf", 74)
        small_font = pygame.font.Font("WDXLLubrifontSC-Regular.ttf", 48)
    except FileNotFoundError:
        font = pygame.font.Font(None, 74) # フォントが見つからない場合はデフォルトに戻す
        small_font = pygame.font.Font(None, 48)

    # ボタンのRect(位置とサイズ)を定義
    play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    how_to_play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
    back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)

    player1 = None
    player2 = None
    all_sprites = None
    players = None
    planets = None
    shots = None
    ADDPLANET = None

    # ゲームループとフレームレート制御
    clock = pygame.time.Clock()
    FPS = 60

    # メインループ
    running = True
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # キーボードイベントの処理ブロック
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    running = False

                if current_game_state == GAME_STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        if player1: 
                            new_shot = player1.shoot()
                            all_sprites.add(new_shot)
                            shots.add(new_shot)
                    
                    if event.key == pygame.K_RETURN: 
                        if player2:
                            new_shot = player2.shoot()
                            all_sprites.add(new_shot)
                            shots.add(new_shot)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 左クリック
                    mouse_pos = event.pos
                    if current_game_state == GAME_STATE_TITLE:
                        if play_button_rect.collidepoint(mouse_pos):
                            # Playボタンがクリックされたらゲーム開始状態へ
                            current_game_state = GAME_STATE_PLAYING
                            # ゲームプレイ用のスプライトなどを初期化
                            player1 = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 80, BLUE, 
                                            pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, 
                                            10, SCREEN_WIDTH, SCREEN_HEIGHT)
                            player2 = Player(SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 80, GREEN, 
                                            pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, 
                                            10, SCREEN_WIDTH, SCREEN_HEIGHT)
                            all_sprites = pygame.sprite.Group()
                            players = pygame.sprite.Group()
                            planets = pygame.sprite.Group()
                            shots = pygame.sprite.Group()
                            all_sprites.add(player1, player2)
                            players.add(player1, player2)
                            
                            # 惑星生成イベント
                            ADDPLANET = pygame.USEREVENT + 1
                            pygame.time.set_timer(ADDPLANET, 1000)

                        elif how_to_play_button_rect.collidepoint(mouse_pos):
                            # 遊び方がクリックされたら説明画面へ
                            current_game_state = GAME_STATE_HOW_TO_PLAY
                    
                    elif current_game_state == GAME_STATE_HOW_TO_PLAY:
                        if back_button_rect.collidepoint(mouse_pos):
                            # 戻るボタンがクリックされたらタイトル画面へ戻る
                            current_game_state = GAME_STATE_TITLE

            # ★ 惑星生成イベントの処理ブロック (MOUSEBUTTONDOWN と同じレベル)
            if current_game_state == GAME_STATE_PLAYING and event.type == ADDPLANET:
                planet_classes = [NormalPlanet, RockPlanet]
                SelectedPlanetClass = random.choice(planet_classes)
                new_planet = SelectedPlanetClass(SCREEN_WIDTH, SCREEN_HEIGHT)
                all_sprites.add(new_planet)
                planets.add(new_planet)
    
        # キー入力の検出とスプライトの更新 (ゲームプレイ中のみ)
        # ここはイベントループの外だが、常に入力をチェックするため必要
        keys = pygame.key.get_pressed()
        if current_game_state == GAME_STATE_PLAYING:
            # player1 と player2 が初期化されていることを確認してから update を呼ぶ
            if player1 and player2:
                players.update(keys)
            planets.update()
            shots.update()

            # 衝突判定
            shot_hit_planets = pygame.sprite.groupcollide(shots, planets, True, False)
            for shot, hit_planet_list in shot_hit_planets.items():
                for planet in hit_planet_list:
                    # shotクラスにdamage属性を追加済みの場合は planet.take_damage(shot.damage)
                    planet.take_damage(shot.damage) # 以前のコメントアウトを外し、shot.damageを使用

        # 描画処理
        screen.fill(GRAY) # 背景は共通

        if current_game_state == GAME_STATE_TITLE:
            # タイトルテキスト (日本語に変更)
            title_text = font.render("惑星破壊シューティングⅡ", True, WHITE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            screen.blit(title_text, title_rect)

            # Playボタンの描画
            pygame.draw.rect(screen, BLUE, play_button_rect)
            play_text = small_font.render("PLAY", True, WHITE)
            play_text_rect = play_text.get_rect(center=play_button_rect.center)
            screen.blit(play_text, play_text_rect)

            # 遊び方ボタンの描画 (日本語に変更)
            pygame.draw.rect(screen, ORANGE, how_to_play_button_rect)
            how_to_play_text = small_font.render("遊び方", True, WHITE)
            how_to_play_text_rect = how_to_play_text.get_rect(center=how_to_play_button_rect.center)
            screen.blit(how_to_play_text, how_to_play_text_rect)

        elif current_game_state == GAME_STATE_PLAYING:
            all_sprites.draw(screen)
        
        elif current_game_state == GAME_STATE_HOW_TO_PLAY:
            # 遊び方説明画面の描画 (日本語に変更)
            how_to_play_title_text = font.render("遊び方", True, WHITE)
            how_to_play_title_rect = how_to_play_title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            screen.blit(how_to_play_title_text, how_to_play_title_rect)

            instructions_text_lines = [
                "プレイヤー1: A/D/W/Sキーで移動, SPACEキーでショット",
                "プレイヤー2: 矢印キーで移動, ENTERキーでショット",
                "上から降ってくる惑星を破壊しましょう！",
                "茶色の惑星は1発、灰色の惑星は3発で破壊できます。"
            ]
            
            y_offset = how_to_play_title_rect.bottom + 50
            for line in instructions_text_lines:
                instruction_text = small_font.render(line, True, WHITE)
                instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(instruction_text, instruction_rect)
                y_offset += 60 # 行間

            # Backボタンの描画
            pygame.draw.rect(screen, BLUE, back_button_rect)
            back_text = small_font.render("戻る", True, WHITE)
            back_text_rect = back_text.get_rect(center=back_button_rect.center)
            screen.blit(back_text, back_text_rect)

        # 画面を更新
        pygame.display.flip()

        # フレームレートの設定
        clock.tick(FPS)

    # 終了処理
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
# main.py
import pygame
import sys
import random

from player import Player
from shot import Shot

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
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# --- main関数 ---
def main():
    # プレイヤーオブジェクトの作成
    player1 = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 80, BLUE, 
                     pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, 
                     10, SCREEN_WIDTH, SCREEN_HEIGHT)

    player2 = Player(SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 80, GREEN, 
                     pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, 
                     10, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Pygameのスプライトグループを作成
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    planets = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    all_sprites.add(player1)
    all_sprites.add(player2)
    players.add(player1)
    players.add(player2)

    # 惑星生成のイベント設定
    ADDPLANET = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDPLANET, 1000)

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
            if event.type == pygame.K_ESCAPE: 
                running = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    running = False

                # ★ ショット発射の処理を追加
                # プレイヤー1 (スペースキー)
                if event.key == pygame.K_SPACE:
                    new_shot = Shot(player1.rect.centerx, player1.rect.top, player1.color)
                    all_sprites.add(new_shot)
                    shots.add(new_shot)
                
                # プレイヤー2 (Enterキー)
                if event.key == pygame.K_RETURN: # EnterキーはK_RETURN
                    new_shot = Shot(player2.rect.centerx, player2.rect.top, player2.color)
                    all_sprites.add(new_shot)
                    shots.add(new_shot)

            if event.type == ADDPLANET:
                planet_classes = [NormalPlanet, RockPlanet]
                SelectedPlanetClass = random.choice(planet_classes)

                new_planet = SelectedPlanetClass(SCREEN_WIDTH, SCREEN_HEIGHT)
                all_sprites.add(new_planet)
                planets.add(new_planet)

        # キー入力の検出
        keys = pygame.key.get_pressed()

        # スプライトを更新
        players.update(keys)
        planets.update()
        shots.update()

        # 描画処理
        screen.fill(GRAY)

        # 全てのスプライトを描画
        all_sprites.draw(screen)

        # 衝突判定
        # shot_hit_planets は {ショットオブジェクト: [衝突した惑星オブジェクト1, 衝突した惑星オブジェクト2, ...]} の辞書を返す
        # True, True はそれぞれ、衝突したショットと惑星を両方ともグループから削除するかどうか
        shot_hit_planets = pygame.sprite.groupcollide(shots, planets, True, False)

        for shot, hit_planet_list in shot_hit_planets.items():
            for planet in hit_planet_list:
                planet.take_damage(shot.damage)

        # 画面を更新
        pygame.display.flip()

        # フレームレートの設定
        clock.tick(FPS)

    # 終了処理
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
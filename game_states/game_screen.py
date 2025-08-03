import pygame
import random
import os
from game_states.game_state import GameState
from player import Player
from shots.shot import Shot
from shots.piercing_shot import PiercingShot
from planets.normal_planet import NormalPlanet
from planets.rock_planet import RockPlanet
from planets.debris import Debris
from planets.ice_planet import IcePlanet
from planets.mid_planet import MidPlanet
from planets.virus_planet import VirusPlanet
from planets.penalty_planet import PenaltyPlanet
from planets.ufo_planet import UFOPlanet
from shots.enemy_shot import EnemyShot
from items.score_item import ScoreItem
from items.power_shot_item import PowerShotItem
from items.heal_item import HealItem
from items.barrier_item import BarrierItem
from items.triple_shot_item import TripleShotItem
from items.piercing_shot_item import PiercingShotItem
from items.speed_up_item import SpeedUpItem
from items.invincibility_item import InvincibilityItem
from items.slow_item import SlowItem

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

class GameScreen(GameState):
  def __init__(self, screen, font, small_font, game_manager):
    super().__init__(screen, font, small_font, game_manager)
    self.screen_width, self.screen_height = self.screen.get_size()

    # 共通背景のロード
    background_path = os.path.join("assets", "images", "background.png")
    self.load_scrolling_background(background_path, speed=0.5)

    # 惑星破壊音のロード
    self.explosion_sound = None
    explosion_sound_path = os.path.join('assets', 'sounds', 'explosion.mp3')
    if os.path.exists(explosion_sound_path):
      self.explosion_sound = pygame.mixer.Sound(explosion_sound_path)
      self.explosion_sound.set_volume(0.1)
    else:
      print(f"惑星破壊音がないよ: {explosion_sound_path}")

    # アイテム取得音のロード 
    self.item_get_sound = None
    item_get_sound_path = os.path.join('assets', 'sounds', 'item_get.mp3')
    if os.path.exists(item_get_sound_path):
      self.item_get_sound = pygame.mixer.Sound(item_get_sound_path)
      self.item_get_sound.set_volume(0.1)
    else:
      print(f"アイテム取得音がないよ: {item_get_sound_path}")

    self.enemy_shots = pygame.sprite.Group()

    self.ADDPLANET = pygame.USEREVENT + 1
    self.ADDITEM = pygame.USEREVENT + 2

    self.all_sprites = pygame.sprite.Group()
    self.players = pygame.sprite.Group()
    self.planets = pygame.sprite.Group()
    self.shots = pygame.sprite.Group()
    self.debris = pygame.sprite.Group()
    self.items = pygame.sprite.Group()

    # 惑星スローダウン関連のプロパティ
    self.is_planet_slowdown_active = False
    self.planet_slowdown_start_time = 0
    self.planet_slowdown_duration = 0
    self.planet_slowdown_factor = 1.0

    self.reset_game()

  def reset_game(self):
    player_size = 70  # 新しいプレイヤーサイズ
    initial_y = self.screen_height - player_size - 10  # 画面下端から少し余裕を持たせる
    
    self.player1 = Player(self.screen_width // 4, initial_y, RED,
                          pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s,
                          10, self.screen_width, self.screen_height, player_id=1, size=player_size)
    self.player2 = Player(self.screen_width * 3 // 4, initial_y, GREEN,
                          pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                          10, self.screen_width, self.screen_height, player_id=2, size=player_size)

    # 既存のグループをクリアしてから新しいプレイヤーを追加
    self.all_sprites.empty()
    self.players.empty()
    self.planets.empty()
    self.shots.empty()
    self.enemy_shots.empty()
    self.debris.empty()
    self.items.empty()

    self.all_sprites.add(self.player1, self.player2)
    self.players.add(self.player1, self.player2)

    # 隕石を生成
    pygame.time.set_timer(self.ADDPLANET, 550)
    # アイテムを生成
    pygame.time.set_timer(self.ADDITEM, 5000)

    # スローダウン効果をリセット
    self.is_planet_slowdown_active = False
    self.planet_slowdown_factor = 1.0

  def handle_event(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        shot = self.player1.shoot()
        if shot:
          self.all_sprites.add(shot)
          self.shots.add(shot)
      if event.key == pygame.K_RETURN:
        shot = self.player2.shoot()
        if shot:
          self.all_sprites.add(shot)
          self.shots.add(shot)
    
    if event.type == self.ADDPLANET:
      # 惑星の種類と重みを定義
      planet_types = [
        NormalPlanet,
        RockPlanet,
        IcePlanet,
        MidPlanet,
        VirusPlanet,
        PenaltyPlanet,
        UFOPlanet,
      ]
      planet_weights = [
        40,
        20,
        20,
        8,
        3,
        4,
        3,
      ]
      
      SelectedPlanetClass = random.choices(planet_types, weights=planet_weights, k=1)[0]

      new_planet = SelectedPlanetClass(self.screen_width, self.screen_height)
      self.all_sprites.add(new_planet)
      self.planets.add(new_planet)

    if event.type == self.ADDITEM:
      # アイテムの種類と重みを定義
      item_types = [
        ScoreItem, 
        PowerShotItem,
        HealItem,
        BarrierItem,
        TripleShotItem,
        PiercingShotItem,
        SpeedUpItem,
        InvincibilityItem,
        SlowItem,
      ]
      item_weights = [
        0,
        0,
        0,
        50,
        0,
        0,
        0,
        50,
        0,
      ]
      
      SelectedItemClass = random.choices(item_types, weights=item_weights, k=1)[0]
      new_item = SelectedItemClass(self.screen_width, self.screen_height)
      self.all_sprites.add(new_item)
      self.items.add(new_item)
  
  def update(self):
    keys = pygame.key.get_pressed()

    self.player1.update(keys)
    self.player2.update(keys)

    current_time = pygame.time.get_ticks()
    # 惑星スローダウンのタイマー処理
    if self.is_planet_slowdown_active:
      if current_time - self.planet_slowdown_start_time > self.planet_slowdown_duration:
        self.is_planet_slowdown_active = False
        self.planet_slowdown_factor = 1.0
        print("惑星のスローダウン効果が終了しました。")


    for planet in self.planets:
      planet.update(self)

    self.shots.update()
    self.enemy_shots.update()
    self.items.update()

    # 破片の更新（引数なしに変更）
    self.debris.update()

    # 破片とプレイヤーの衝突判定（修正）
    debris_hit_players = pygame.sprite.groupcollide(self.debris, self.players, True, False)
    for debris_piece, hit_players_list in debris_hit_players.items():
      for player in hit_players_list:
        if player.is_alive():
          damage_from_debris = debris_piece.damage_amount
          player.take_damage(damage_from_debris)

    self.update_background()

    # 衝突判定(ショットと惑星)
    for shot in self.shots.copy():
      if not shot.alive():
        continue
        
      planets_hit_by_shot = pygame.sprite.spritecollide(shot, self.planets, False, pygame.sprite.collide_mask)
      for planet in planets_hit_by_shot:
        if not planet.alive():
          continue
          
        # 貫通ショットの場合
        if isinstance(shot, PiercingShot):
          if planet not in shot.hit_enemies:
            planet_destroyed = planet.take_damage(shot.damage)
            shot.hit_enemies.add(planet)

            if planet_destroyed:
              destroying_player = shot.owner_player
              if destroying_player:
                destroying_player.score += planet.score_value
                if destroying_player.score < 0:
                  destroying_player.score = 0
              
              if self.explosion_sound:
                self.explosion_sound.play()
              planet.on_destroyed(self, destroying_player)
              planet.kill()

        else:
          planet_destroyed = planet.take_damage(shot.damage)
          shot.kill()

          if planet_destroyed:
            destroying_player = shot.owner_player
            if destroying_player:
              destroying_player.score += planet.score_value
              if destroying_player.score < 0:
                destroying_player.score = 0
            
            if self.explosion_sound:
              self.explosion_sound.play()
            planet.on_destroyed(self, destroying_player)
            planet.kill()
          
          break

    # 敵のショットがプレイヤーに当たる衝突判定
    enemy_shot_hit_players = pygame.sprite.groupcollide(self.enemy_shots, self.players, True, False)
    for enemy_shot, hit_players_list in enemy_shot_hit_players.items():
      for player in hit_players_list:
        if player.is_alive():
          player.take_damage(enemy_shot.damage)

    # 惑星とプレイヤーの当たり判定
    player_hit_planets = pygame.sprite.groupcollide(self.players, self.planets, False, True)
    for player, hit_planets_list in player_hit_planets.items():
      for planet in hit_planets_list:
        if player.is_alive():
          damage_from_planet = 1
          player.take_damage(damage_from_planet)

    # プレイヤーとアイテムの衝突判定
    player_hit_items = pygame.sprite.groupcollide(self.players, self.items, False, True)
    for player, hit_items_list in player_hit_items.items():
      for item in hit_items_list:
        if player.is_alive():
          item.apply_effect(player, self)
          self.all_sprites.remove(item)
          if self.item_get_sound:
            self.item_get_sound.play()
    
    # ゲームオーバー判定
    p1_game_over = (self.player1.hp <= 0)
    p2_game_over = (self.player2.hp <= 0)

    if p1_game_over and p2_game_over:
      print("1P2P共にゲームオーバー")
      self.game_manager.change_state("game_over", self.player1.score, self.player2.score)
    elif p1_game_over:
      self.player1.kill()
    elif p2_game_over:
      self.player2.kill()
  
  # 惑星スローダウンをアクティブにするメソッド
  def activate_planet_slowdown(self, duration_ms, slow_factor):
    self.is_planet_slowdown_active = True
    self.planet_slowdown_start_time = pygame.time.get_ticks()
    self.planet_slowdown_duration = duration_ms
    self.planet_slowdown_factor = slow_factor
    print(f"惑星の速度が {slow_factor} 倍になりました！")
  
  def draw(self):
    self.draw_background()

    for sprite in self.all_sprites:
      if isinstance(sprite, Player):
        continue
      self.screen.blit(sprite.image, sprite.rect)

    if self.player1.is_alive():
      self.player1.draw(self.screen)
    if self.player2.is_alive():
      self.player2.draw(self.screen)

    player1_score_text = self.small_font.render(f"P1スコア: {self.player1.score}", True, RED)
    player1_hp_text = self.small_font.render(f"P1HP: {self.player1.hp}", True, RED)
    self.screen.blit(player1_score_text, (10, 10))
    self.screen.blit(player1_hp_text, (10, 60))
    
    player2_score_text = self.small_font.render(f"P2スコア: {self.player2.score}", True, GREEN)
    player2_hp_text = self.small_font.render(f"P2HP: {self.player2.hp}", True, GREEN)
    self.screen.blit(player2_score_text, (self.screen_width - player2_score_text.get_width() - 10, 10))
    self.screen.blit(player2_hp_text, (self.screen_width - player2_hp_text.get_width() - 10, 60))

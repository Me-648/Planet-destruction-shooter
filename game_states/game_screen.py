import pygame
import random
import os
from game_states.game_state import GameState
from player import Player
from shot import Shot
from planets.normal_planet import NormalPlanet
from planets.rock_planet import RockPlanet

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

class GameScreen(GameState):
  def __init__(self, screen, font, small_font, game_manager):
    super().__init__(screen, font, small_font, game_manager)
    self.screen_width, self.screen_height = self.screen.get_size()

    # 惑星破壊音のロード
    self.explosion_sound = None
    explosion_sound_path = os.path.join('assets', 'sounds', 'explosion.mp3')
    if os.path.exists(explosion_sound_path):
      self.explosion_sound = pygame.mixer.Sound(explosion_sound_path)
      self.explosion_sound.set_volume(0.1)
    else:
      print(f"惑星破壊音がないよ: {explosion_sound_path}")

    self.ADDPLANET = pygame.USEREVENT + 1

    self.all_sprites = pygame.sprite.Group()
    self.players = pygame.sprite.Group()
    self.planets = pygame.sprite.Group()
    self.shots = pygame.sprite.Group()

    self.reset_game()

  def reset_game(self):
    self.player1 = Player(self.screen_width // 4, self.screen_height - 80, BLUE,
                            pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s,
                            10, self.screen_width, self.screen_height)
    self.player2 = Player(self.screen_width * 3 // 4, self.screen_height - 80, GREEN,
                            pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                            10, self.screen_width, self.screen_height)

    # 既存のグループをクリアしてから新しいプレイヤーを追加
    self.all_sprites.empty()
    self.players.empty()
    self.planets.empty()
    self.shots.empty()

    self.all_sprites.add(self.player1, self.player2)
    self.players.add(self.player1, self.player2)

    # 隕石を生成
    pygame.time.set_timer(self.ADDPLANET, 400)

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
      planet_class = [NormalPlanet, RockPlanet]
      SelectedPlanetClass = random.choice(planet_class)
      new_planet = SelectedPlanetClass(self.screen_width, self.screen_height)
      self.all_sprites.add(new_planet)
      self.planets.add(new_planet)
  
  def update(self):
    keys = pygame.key.get_pressed()

    self.player1.update(keys)
    self.player2.update(keys)

    self.planets.update()
    self.shots.update()

    # 衝突判定
    shot_hit_planets = pygame.sprite.groupcollide(self.shots, self.planets, True, False)
    for shot, hit_planets_list in shot_hit_planets.items():
      for planet in hit_planets_list:
        planet.take_damage(shot.damage)
        if planet.hp <= 0:
          if hasattr(shot, 'owner_player') and shot.owner_player is not None:
            shot.owner_player.score += planet.score_value
            print(f"{shot.owner_player.color}プレイヤーが{planet.score_value}スコア獲得！合計: {shot.owner_player.score}")
          if self.explosion_sound:
            self.explosion_sound.play()
            # planet.on_destroyed()


    # 当たり判定
    player_hit_planets = pygame.sprite.groupcollide(self.players, self.planets, False, True)
    for player, hit_planets_list in player_hit_planets.items():
      for planet in hit_planets_list:
        if player.take_damage(): # プレイヤーのtake_damageメソッドを呼び出す
          pass
    
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
  
  def draw(self):
    self.screen.fill(GRAY)
    self.all_sprites.draw(self.screen)

    player1_score_text = self.small_font.render(f"P1スコア: {self.player1.score}", True, BLUE)
    player1_hp_text = self.small_font.render(f"P1HP: {self.player1.hp}", True, BLUE)
    self.screen.blit(player1_score_text, (10, 10))
    self.screen.blit(player1_hp_text, (10, 60))
    
    player2_score_text = self.small_font.render(f"P2スコア: {self.player2.score}", True, GREEN)
    player2_hp_text = self.small_font.render(f"P2HP: {self.player2.hp}", True, GREEN)
    self.screen.blit(player2_score_text, (self.screen_width - player2_score_text.get_width() - 10, 10))
    self.screen.blit(player2_hp_text, (self.screen_width - player2_hp_text.get_width() - 10, 60))

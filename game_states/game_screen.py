import pygame
import random
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

    pygame.time.set_timer(self.ADDPLANET, 1000)

  def handle_event(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        new_shot = self.player1.shoot()
        self.all_sprites.add(new_shot)
        self.shots.add(new_shot)
      if event.key == pygame.K_RETURN:
        new_shot = self.player2.shoot()
        self.all_sprites.add(new_shot)
        self.shots.add(new_shot)
    
    if event.type == self.ADDPLANET:
      planet_class = [NormalPlanet, RockPlanet]
      SelectedPlanetClass = random.choice(planet_class)
      new_planet = SelectedPlanetClass(self.screen_width, self.screen_height)
      self.all_sprites.add(new_planet)
      self.planets.add(new_planet)
  
  def update(self):
    keys = pygame.key.get_pressed()
    self.players.update(keys)
    self.planets.update()
    self.shots.update()

    # 衝突判定
    shot_hit_planets = pygame.sprite.groupcollide(self.shots, self.planets, True, False)
    for shot, hit_planets_list in shot_hit_planets.items():
      for planet in hit_planets_list:
        planet.take_damage(shot.damage)
  
  def draw(self):
    self.screen.fill(GRAY)
    self.all_sprites.draw(self.screen)


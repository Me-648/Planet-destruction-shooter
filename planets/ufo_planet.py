import pygame
import os
import random
from .planet_base import BasePlanet
from shots.enemy_shot import EnemyShot

class UFOPlanet(BasePlanet):
  def __init__(self, screen_width, screen_height):
    size = 70
    color = (150, 150, 150)
    speed = random.uniform(1.5, 3)
    hp = 2
    score_value = 200

    image_path = 'planet_ufo.png'

    super().__init__(screen_width, screen_height, size, color, hp, speed, score_value, image_path)

    # UFO固有のプロパティ
    self.attack_interval = random.randint(40, 120)
    self.attack_timer = 0
    self.shot_speed = 4

    # ジグザグ移動用プロパティ  
    self.zigzag_speed = random.uniform(0.5, 2)
    self.zigzag_direction = random.choice([-1, 1])
    self.zigzag_range = 150
    self.initial_x = self.rect.x
  
  def update(self, game_screen_instance):
    super().update()
    self.attack_timer += 1

    self.rect.x += self.zigzag_direction * self.zigzag_speed

    if self.rect.x > self.initial_x + self.zigzag_range:
      self.zigzag_direction = -1
    elif self.rect.x < self.initial_x - self.zigzag_range:
      self.zigzag_direction = 1

    self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))

    if self.rect.top < self.screen_height and self.rect.bottom > 0:
      if self.attack_timer >= self.attack_interval:
        self.attack_timer = 0
        self.attack(game_screen_instance)

  
  def attack(self, game_screen_instance):
    player1_alive = game_screen_instance.player1.is_alive()
    player2_alive = game_screen_instance.player2.is_alive()

    target_player_rect = None
              
    if player1_alive and player2_alive:
      dist_p1 = pygame.math.Vector2(self.rect.center).distance_to(game_screen_instance.player1.rect.center)
      dist_p2 = pygame.math.Vector2(self.rect.center).distance_to(game_screen_instance.player2.rect.center)

      if dist_p1 < dist_p2:
        target_player_rect = game_screen_instance.player1.rect
      else:
        target_player_rect = game_screen_instance.player2.rect
    elif player1_alive:
      target_player_rect = game_screen_instance.player1.rect
    elif player2_alive:
      target_player_rect = game_screen_instance.player2.rect
    
    if target_player_rect:
      new_enemy_shot = EnemyShot(
        self.rect.centerx,
        self.rect.centery + self.rect.height // 2,
        self.shot_speed,
        target_player_rect
      )

      game_screen_instance.all_sprites.add(new_enemy_shot)
      game_screen_instance.enemy_shots.add(new_enemy_shot)

  def on_destroyed(self, game_screen_instance, destroying_player):
    pass
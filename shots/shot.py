import pygame

class Shot(pygame.sprite.Sprite):
  def __init__(self, x, y, color, owner_player=None, damage=1):
    super().__init__()

    self.image = pygame.Surface([5, 15]) # ショットの見た目を細長い四角形にする
    self.image.fill(color) # ショットの色

    self.rect = self.image.get_rect()
    self.rect.centerx = x # ショットのX座標をプレイヤーの中心に合わせる
    self.rect.bottom = y # ショットのY座標をプレイヤーの上端に合わせる

    self.speed = -15 # ショットの速度
    self.damage = damage # ショットのダメージ

    self.owner_player = owner_player

  def update(self):
    # ショットを移動させる
    self.rect.y += self.speed
        
    # 画面上部まで行ったら消える
    if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
      self.kill()
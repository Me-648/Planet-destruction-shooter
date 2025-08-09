# ui/item_effect_ui.py
import pygame
import os
from typing import Dict, List, Tuple

class ItemEffectUI:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # アイテムアイコンの設定
        self.icon_size = 32
        self.icon_spacing = 40  # アイコン間の間隔
        self.bar_height = 4     # 効果時間バーの高さ
        self.bar_width = self.icon_size  # バーの幅はアイコンと同じ
        
        # アイテムアイコンの辞書
        self.item_icons: Dict[str, pygame.Surface] = {}
        self.load_item_icons()
        
        # 色の設定
        self.bar_colors = {
            'background': (60, 60, 60),      # 背景色（グレー）
            'time_high': (0, 255, 0),        # 残り時間多い（緑）
            'time_medium': (255, 255, 0),    # 残り時間中程度（黄）
            'time_low': (255, 0, 0),         # 残り時間少ない（赤）
            'uses': (0, 150, 255),           # 使用回数制限（青）
            'count': (255, 0, 255),          # 回数制限（マゼンタ）
        }
    
    def load_item_icons(self):
        icon_mappings = {
            'power_shot': 'items/item_powershot.png',
            'triple_shot': 'items/item_triple_shot.png',
            'piercing_shot': 'items/item_piercing_shot.png',
            'invincibility': 'items/item_invincibility.png',
            'speed_up': 'items/item_speed_up.png',
            'barrier': 'items/item_barrier.png',
            'slow': 'items/item_slow.png',
        }
        
        for effect_name, image_path in icon_mappings.items():
            full_path = os.path.join('assets', 'images', image_path)
            
            if os.path.exists(full_path):
                try:
                    # 画像を読み込んでサイズ調整
                    original_image = pygame.image.load(full_path).convert_alpha()
                    scaled_image = pygame.transform.scale(original_image, (self.icon_size, self.icon_size))
                    self.item_icons[effect_name] = scaled_image
                except pygame.error:
                    print(f"アイコン読み込みエラー: {full_path}")
                    self.item_icons[effect_name] = self.create_placeholder_icon(effect_name)
            else:
                print(f"アイコンファイルが見つかりません: {full_path}")
                self.item_icons[effect_name] = self.create_placeholder_icon(effect_name)
    
    def create_placeholder_icon(self, effect_name: str) -> pygame.Surface:
        placeholder_colors = {
            'power_shot': (255, 100, 100),
            'triple_shot': (100, 255, 255),
            'piercing_shot': (255, 255, 100),
            'invincibility': (255, 255, 255),
            'speed_up': (255, 255, 0),
            'barrier': (100, 100, 255),
            'slow': (173, 216, 230),
        }
        
        surface = pygame.Surface((self.icon_size, self.icon_size))
        color = placeholder_colors.get(effect_name, (128, 128, 128))
        surface.fill(color)
        return surface
    
    def get_active_effects(self, player, game_screen=None) -> List[Dict]:
        active_effects = []
        current_time = pygame.time.get_ticks()
        
        # 時間制限アイテムの効果
        time_based_effects = [
            {
                'name': 'power_shot',
                'active': player.is_power_shot_active,
                'start_time': getattr(player, 'power_shot_start_time', 0),
                'duration': getattr(player, 'power_shot_duration', 0),
                'type': 'time'
            },
            {
                'name': 'triple_shot',
                'active': player.is_triple_shot_active,
                'start_time': getattr(player, 'triple_shot_start_time', 0),
                'duration': getattr(player, 'triple_shot_duration', 0),
                'type': 'time'
            },
            {
                'name': 'invincibility',
                'active': player.is_item_invincible_active,
                'start_time': getattr(player, 'item_invincibility_start_time', 0),
                'duration': getattr(player, 'item_invincibility_duration', 0),
                'type': 'time'
            },
            {
                'name': 'speed_up',
                'active': player.is_speed_up_active,
                'start_time': getattr(player, 'speed_up_start_time', 0),
                'duration': getattr(player, 'speed_up_duration', 0),
                'type': 'time'
            }
        ]
        
        # ゲーム全体に影響する効果（Slowアイテム）
        if game_screen and hasattr(game_screen, 'is_planet_slowdown_active'):
            if game_screen.is_planet_slowdown_active:
                elapsed_time = current_time - game_screen.planet_slowdown_start_time
                remaining_time = max(0, game_screen.planet_slowdown_duration - elapsed_time)
                progress = remaining_time / game_screen.planet_slowdown_duration if game_screen.planet_slowdown_duration > 0 else 0
                
                # Slowアイテムは最後に取得したプレイヤーに表示（または両方に表示）
                time_based_effects.append({
                    'name': 'slow',
                    'active': True,
                    'start_time': game_screen.planet_slowdown_start_time,
                    'duration': game_screen.planet_slowdown_duration,
                    'progress': progress,
                    'type': 'time'
                })
        
        # 使用回数制限アイテムの効果
        use_based_effects = [
            {
                'name': 'piercing_shot',
                'active': player.is_piercing_shot_active,
                'current_uses': getattr(player, 'piercing_shot_count', 0),
                'max_uses': getattr(player, 'piercing_shot_max_uses', 3),
                'type': 'uses'
            }
        ]
        
        # 回数制限効果（バリア）
        count_based_effects = [
            {
                'name': 'barrier',
                'active': getattr(player, 'barrier_count', 0) > 0,
                'current_count': getattr(player, 'barrier_count', 0),
                'max_count': getattr(player, 'max_barrier_count', 3),
                'type': 'count'
            }
        ]
        
        # アクティブな効果のみを追加
        for effect in time_based_effects:
            if effect['active']:
                # Slowアイテムの場合は既に進行度が計算済み
                if 'progress' not in effect:
                    elapsed_time = current_time - effect['start_time']
                    remaining_time = max(0, effect['duration'] - elapsed_time)
                    effect['progress'] = remaining_time / effect['duration'] if effect['duration'] > 0 else 0
                active_effects.append(effect)
        
        for effect in use_based_effects:
            if effect['active'] and effect['current_uses'] > 0:
                effect['progress'] = effect['current_uses'] / effect['max_uses']
                active_effects.append(effect)
        
        for effect in count_based_effects:
            if effect['active'] and effect['current_count'] > 0:
                effect['progress'] = effect['current_count'] / effect['max_count']
                active_effects.append(effect)
        
        return active_effects
    
    def get_bar_color(self, effect_type: str, progress: float) -> Tuple[int, int, int]:
        if effect_type == 'uses':
            return self.bar_colors['uses']
        elif effect_type == 'count':
            return self.bar_colors['count']
        elif effect_type == 'persistent':
            return self.bar_colors['time_high']
        else:  # time-based
            if progress > 0.6:
                return self.bar_colors['time_high']
            elif progress > 0.3:
                return self.bar_colors['time_medium']
            else:
                return self.bar_colors['time_low']
    
    def draw_player_effects(self, screen: pygame.Surface, player, start_x: int, start_y: int, game_screen=None):
        active_effects = self.get_active_effects(player, game_screen)
        
        if not active_effects:
            return
        
        for i, effect in enumerate(active_effects):
            # アイコンの位置計算
            icon_x = start_x + (i * self.icon_spacing)
            icon_y = start_y
            
            # アイコンを描画
            if effect['name'] in self.item_icons:
                screen.blit(self.item_icons[effect['name']], (icon_x, icon_y))
            
            # 効果時間バーを描画
            bar_x = icon_x
            bar_y = icon_y + self.icon_size + 2
            
            # 背景バー（グレー）
            pygame.draw.rect(screen, self.bar_colors['background'], 
                           (bar_x, bar_y, self.bar_width, self.bar_height))
            
            # 進行度バー
            if effect['progress'] > 0:
                progress_width = int(self.bar_width * effect['progress'])
                bar_color = self.get_bar_color(effect['type'], effect['progress'])
                pygame.draw.rect(screen, bar_color,
                               (bar_x, bar_y, progress_width, self.bar_height))
            
            # 回数制限アイテムの場合、数字も表示
            if effect['type'] in ['uses', 'count']:
                current_value = effect.get('current_uses', effect.get('current_count', 0))
                if current_value > 0:
                    font = pygame.font.Font(None, 16)
                    uses_text = font.render(str(current_value), True, (255, 255, 255))
                    text_rect = uses_text.get_rect()
                    text_rect.center = (icon_x + self.icon_size // 2, icon_y + self.icon_size // 2)
                    screen.blit(uses_text, text_rect)
    
    def draw_all_effects(self, screen: pygame.Surface, player1, player2, game_screen=None):
        # Player1の効果（左側）
        p1_start_x = 10
        p1_start_y = 120  # HP表示の下
        self.draw_player_effects(screen, player1, p1_start_x, p1_start_y, game_screen)
        
        # Player2の効果（右側）
        # Player2の効果は右端から左に向かって表示
        active_effects_p2 = self.get_active_effects(player2, game_screen)
        if active_effects_p2:
            total_width = len(active_effects_p2) * self.icon_spacing - (self.icon_spacing - self.icon_size)
            p2_start_x = self.screen_width - total_width - 10
            p2_start_y = 120
            self.draw_player_effects(screen, player2, p2_start_x, p2_start_y, game_screen)
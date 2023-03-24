import time

import arcade
from arcade import SpriteList

from .player import Player, Direction, PlayerAnimationState
from .projectile import Projectile


class AWeapon(arcade.Sprite):
    SPRITE_SCALE = 1.5

    def __init__(self, player: Player, player_projectile_list: SpriteList, magazine_size=0, reload_time=0,
                 weapon_range=0):
        super().__init__()
        self.reload_time = reload_time
        self.weapon_range = weapon_range
        self.magazine_size = magazine_size
        self.current_ammo = magazine_size
        self.texture = self.load_textures()
        self.scale = AWeapon.SPRITE_SCALE
        self.player = player
        self.player_direction = self.player.get_direction()
        self.player_x, self.player_y = self.player.get_position()
        self.player_projectile_list = player_projectile_list
        self.reloading = False
        self.real_time = time.localtime()
        self.reloading_start_time = self.real_time

    def update(self):
        self.real_time = time.localtime()
        if self.reloading and abs(self.real_time.tm_sec - self.reloading_start_time.tm_sec) >= self.reload_time:
            self.reloading = False
            self.current_ammo = self.magazine_size
        WEAPON_X_OFFSET = 27
        WEAPON_INITIAL_OFFSET = 37
        WEAPON_WALKING_OFFSET = 13
        self.player_direction = self.player.get_direction()
        self.player_x, self.player_y = self.player.get_position()
        self.center_x = self.player_x
        self.center_y = self.player_y - WEAPON_INITIAL_OFFSET
        if PlayerAnimationState.WALK.value[0] == self.player.get_state().value[0]:
            self.center_y = self.center_y - WEAPON_WALKING_OFFSET
        else:
            if self.player.get_direction().value[0] is Direction.LEFT.value[0]:
                self.center_x += WEAPON_X_OFFSET
            else:
                self.center_x -= WEAPON_X_OFFSET

    def shoot(self, target_x, target_y):
        if not self.reloading:
            bullet_path = ":data:bullet/0.png"
            scale = 1
            self.player_projectile_list.append(
                Projectile(self.center_x, self.center_y, target_x, target_y, bullet_path, scale, self.weapon_range)
            )
            self.current_ammo -= 1
            if self.current_ammo == 0:
                self.reloading = True
                self.reloading_start_time = self.real_time

    def load_textures(self):
        raise NotImplementedError("load_textures() not implemented")

    def get_kind(self):
        return "weapon"


class Skull(AWeapon):
    Sprite_Scale = 1.5
    COIN_PATH = ":data:player/skull/0.png"

    def __init__(self, player: Player, player_projectile_list: SpriteList):
        super().__init__(player, player_projectile_list, magazine_size=6, reload_time=2, weapon_range=600)

    def load_textures(self):
        """loads the right textures of the sprite
        """
        texture = arcade.load_texture(Skull.COIN_PATH)
        return texture

    def get_kind(self):
        return "skull"

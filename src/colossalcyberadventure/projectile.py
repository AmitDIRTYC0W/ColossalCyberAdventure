from math import atan2, degrees

import time
import arcade
from pyglet.math import Vec2


class Projectile(arcade.Sprite):
    Sprite_Path = None
    SPEED = 15

    def __init__(self, origin_x: float, origin_y: float, target_x: float, target_y: float, Sprite_Path: str,
                 SPRITE_SCALE=2.5, time_to_live=1):
        self.Sprite_Path = Sprite_Path
        super().__init__(self.Sprite_Path, scale=SPRITE_SCALE)
        self.start_time = time.localtime()
        self.time_to_live = time_to_live
        self.center_x = origin_x
        self.center_y = origin_y
        direction = Vec2(target_x - origin_x, target_y - origin_y).normalize() * Vec2(Projectile.SPEED,
                                                                                      Projectile.SPEED)
        self.change_x = direction.x
        self.change_y = direction.y
        self.angle = degrees(atan2(direction.y, direction.x))
        self.time = self.start_time

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.time = time.localtime()
        if abs(self.time.tm_sec - self.start_time.tm_sec) >= self.time_to_live:
            self.remove_from_sprite_lists()
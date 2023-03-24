from math import atan2, degrees
from math import sqrt

import arcade
from pyglet.math import Vec2


class Projectile(arcade.Sprite):
    Sprite_Path = None
    SPEED = 15

    def __init__(self, origin_x: float, origin_y: float, target_x: float, target_y: float, sprite_path: str,
                 sprite_scale=2.5, distance=700):
        self.Sprite_Path = sprite_path
        super().__init__(self.Sprite_Path, scale=sprite_scale)
        self.distance = 0
        self.max_distance = distance
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.center_x = origin_x
        self.center_y = origin_y
        direction = Vec2(target_x - origin_x, target_y - origin_y).normalize() * Projectile.SPEED
        self.change_x = direction.x
        self.change_y = direction.y
        self.angle = -degrees(atan2(direction.y, direction.x))

    def update(self):
        self.distance = sqrt(abs(self.origin_x - self.center_x) ** 2 + abs(self.origin_y - self.center_y) ** 2)
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.distance >= self.max_distance:
            self.remove_from_sprite_lists()

from math import atan2, degrees

import arcade
from pyglet.math import Vec2

from colossalcyberadventure.player import Player


class Bullet(arcade.Sprite):
    SPEED = 15
    SPRITE_PATH = "resources/bullet/0.png"

    def __init__(self, origin_x: float, origin_y: float, target_x: float, target_y: float):
        super().__init__(Bullet.SPRITE_PATH)

        self.center_x = origin_x
        self.center_y = origin_y
        direction = Vec2(target_x - origin_x, target_y - origin_y).normalize() * Vec2(Bullet.SPEED, Bullet.SPEED)
        self.change_x = direction.x
        self.change_y = direction.y
        self.angle = degrees(atan2(direction.y, direction.x))

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

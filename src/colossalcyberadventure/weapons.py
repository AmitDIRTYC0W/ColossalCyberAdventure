import math

import arcade

from src.colossalcyberadventure.entity import IEntity


class Weapon(arcade.Sprite):
    def __init__(self, owner: IEntity):
        super().__init__(arcade.Sprite, filename="resources/weapons/laser_pistol.png", scale=0.1)
        self.flipped_horizontally = False
        self.owner = owner
        self.owner_x = owner.get_position()[0]
        self.owner_y = owner.get_position()[1]
        self.center_x = -1  # placeholder
        self.center_y = -1  # placeholder

    def update(self):
        self.center_x = self.owner.get_position()[0] + 15
        self.center_y = self.owner.get_position()[1] - 45



    def update_weapon_angle(self, x, y):
        if x - self.center_x > 0:
            self.angle = math.atan2(y - self.center_y, x - self.center_x) * 180/math.pi
        if x - self.center_x < 0:
            self.flipped_horizontally = True
            self.angle = math.atan2(y - self.center_y, x - self.center_x) * 180 / math.pi




from typing import List

import arcade.camera
from arcade import SpriteList, Sprite
from pyglet.math import Vec2
from pytiled_parser.tiled_object import Point

from globals import *


class GameCam(arcade.camera.Camera):

    def __init__(self, width, height, player):
        super().__init__()
        self.player = player

    def zoom(self):
        pass

    def get_sprites_at_point(self, point: "Point", sprite_list: "SpriteList") -> List["Sprite"]:
        pass

    def center_camera_on_player(self):
        screen_center_x = self.player.center_x - (self.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        if screen_center_x > map_width - self.viewport_width:
            screen_center_x = map_width - self.viewport_width
        if screen_center_y > map_height - self.viewport_height:
            screen_center_y = map_height - self.viewport_height

        player_centered = Vec2(screen_center_x, screen_center_y)

        self.move_to(player_centered)

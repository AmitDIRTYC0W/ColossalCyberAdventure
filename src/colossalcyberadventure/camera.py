import arcade.camera
from pyglet.math import Vec2

from constants import *


class GameCam(arcade.camera.Camera):

    def __init__(self, width, height, player):
        super().__init__(width, height)
        self.player = player

    def zoom(self, change: float):
        pass

    def center_camera_on_player(self):
        screen_center_x = self.player.center_x - (self.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        if screen_center_x > MAP_WIDTH - self.viewport_width:
            screen_center_x = MAP_WIDTH - self.viewport_width
        if screen_center_y > MAP_HEIGHT - self.viewport_height:
            screen_center_y = MAP_HEIGHT - self.viewport_height

        player_centered = Vec2(screen_center_x, screen_center_y)

        self.move_to(player_centered)

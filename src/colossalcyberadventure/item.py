import arcade
from src.colossalcyberadventure.constants import *


class Coin(arcade.Sprite):
    def __init__(self, x_position: float, y_position: float):
        super().__init__()
        self.texture = arcade.load_texture("resources/items/coin.png")
        self.scale = 0.4
        self.center_x = x_position
        self.center_y = y_position


class HealthShroom(arcade.Sprite):
    def __init__(self, x_position: float, y_position: float):
        super().__init__()
        self.texture = arcade.load_texture("resources/items/HPSHROOM.png")
        self.scale = 0.4
        self.center_x = x_position
        self.center_y = y_position


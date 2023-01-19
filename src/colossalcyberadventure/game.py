import arcade
import arcade.gui
from arcade import key as k

from colossalcyberadventure.camera import GameCam
from colossalcyberadventure.player import Player
from constants import *


class GameView(arcade.View):
    """View of the actual game

    Attributes
    ----------
    player: Player
    keyboard_state: dict[int, bool]
    map: arcade.tilemap.TileMap
        The full map
    scene: arcade.scene.Scene
    """

    BACKGROUND_COLOR = arcade.color.JET
    MAP_PATH = "resources/map/map.tmj"

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False}
        self.camera = GameCam(self.window.width, self.window.height, self.player)
        self.map = arcade.load_tilemap(GameView.MAP_PATH, TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.map)

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()
        self.player.draw()

    def on_update(self, delta_time: float):
        self.player.update_player_speed(self.keyboard_state)
        self.player.update_animation()
        self.player.update()
        self.camera.center_camera_on_player()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = True

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = False

import arcade

from arcade import key as k

from colossalcyberadventure.player import Player
from constants import *


class ColossalCyberAdventure(arcade.Window):
    TITLE = "Colossal Cyber Adventure"
    BACKGROUND_COLOR = arcade.color.AMAZON

    def __init__(self):
        super().__init__(title=ColossalCyberAdventure.TITLE, fullscreen=True)

        arcade.set_background_color(ColossalCyberAdventure.BACKGROUND_COLOR)

    def setup(self):
        """Set up window

        Sets up window. Call this again to restart game.
        """
        self.show_view(GameView())


class GameView(arcade.View):
    """View of the actual game
    """

    BACKGROUND_COLOR = arcade.color.JET
    MAP_PATH = "resources/map.tmx"

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False}
        self.camera = arcade.camera.Camera(self.window.width, self.window.height)
        self.tile_map = arcade.load_tilemap(GameView.MAP_PATH, TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

    def on_draw(self):
        self.clear()

        self.player.draw()

    def on_update(self, delta_time: float):
        self.player.update_player_speed(self.keyboard_state)
        self.player.update_animation()
        self.player.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = True

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = False

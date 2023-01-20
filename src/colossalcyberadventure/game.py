import arcade

from arcade import key as k, SpriteList
from pyglet.math import Vec2

from colossalcyberadventure.bullet import Bullet
from colossalcyberadventure.camera import GameCam
from colossalcyberadventure.player import Player
from constants import *


class ColossalCyberAdventure(arcade.Window):
    """Main window class. (0, 0) at the bottom left."""
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
        self.bullet_list = SpriteList()
        # self.bullet_list.append(Bullet(10, 10, 100, 100))
        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False}
        self.camera = GameCam(self.window.width, self.window.height, self.player)
        self.map = arcade.load_tilemap(GameView.MAP_PATH, TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.map)

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

    def mouse_to_world_position(self, click_x: float, click_y: float) -> Vec2:
        return Vec2(self.camera.position.x + click_x, self.camera.position.y + click_y)

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()
        self.player.draw()
        self.bullet_list.draw()
        self.player.draw_health_bar()

    def on_update(self, delta_time: float):
        self.bullet_list.update()
        self.player.update_player_speed(self.keyboard_state)
        self.player.update_animation()
        self.player.update()
        self.camera.center_camera_on_player()
        self.player.health_bar.set_inner_rectangle_width()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = True

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        world_pos = self.mouse_to_world_position(x, y)
        self.bullet_list.append(Bullet(self.player.center_x, self.player.center_y, world_pos.x, world_pos.y))

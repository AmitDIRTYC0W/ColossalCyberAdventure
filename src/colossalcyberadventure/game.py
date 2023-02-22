from math import floor
from pathlib import Path

import arcade
from pytiled_parser import parse_world

from arcade import SpriteList, Scene
from pyglet.math import Vec2
import arcade.gui
from arcade import key as k

from src.colossalcyberadventure.bullet import Bullet
from src.colossalcyberadventure.camera import GameCam
from src.colossalcyberadventure.player import Player
from globals import *


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
    WORLD_PATH = "resources/map/map.world"
    MAP_PARTIAL_WIDTH = 2560
    MAP_PARTIAL_HEIGHT = 1440

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.bullet_list = SpriteList()
        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False, k.Q: False}
        self.camera = GameCam(self.window.width, self.window.height, self.player)
        # self.map = arcade.load_tilemap(GameView.MAP_PATH, TILE_SCALING)
        # self.scene = arcade.Scene.from_tilemap(self.map)
        self.world = parse_world(Path(GameView.WORLD_PATH))
        tilemap = arcade.tilemap.TileMap(map_file=self.world.maps[0].map_file)
        # y-x.tmx
        self.scene = arcade.Scene()
        for spritelist in self.get_scene_from_partial_tilemap(0, 0).sprite_lists:
            self.scene.add_sprite_list("terst", True, spritelist)

        self.flag = False

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

    def get_scene_from_partial_tilemap(self, x, y):
        return arcade.Scene.from_tilemap(
            arcade.load_tilemap(self.world.maps[x * 30 + y].map_file, use_spatial_hash=True,
                                offset=Vec2(x * 2560, y * 1440), scaling=2.0))

    def connect_scenes(self, other_scene: Scene, key: str):
        for spritelist in other_scene.sprite_lists:
            self.scene.add_sprite_list(key, True, spritelist)

    def mouse_to_world_position(self, click_x: float, click_y: float) -> Vec2:
        """Converts the position of a click to the actual world position

        Parameters
        ----------
        click_x : float
        click_y : float

        Returns
        -------
        Vec2
            x -> world x, y -> world y
        """
        return Vec2(self.camera.position.x + click_x, self.camera.position.y + click_y)

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()
        self.player.draw()
        self.bullet_list.draw()

    def on_update(self, delta_time: float):
        # load map
        map_x = round(self.player.center_x / GameView.MAP_PARTIAL_WIDTH)
        map_y = round(self.player.center_y / GameView.MAP_PARTIAL_HEIGHT)
        if self.player.center_x > 2400 and not self.flag:
            s = self.get_scene_from_partial_tilemap(1, 0)
            self.connect_scenes(s, "1234")
            self.flag = True

        if self.keyboard_state[k.Q]:
            quit()
        self.bullet_list.update()
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

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        world_pos = self.mouse_to_world_position(x, y)
        self.bullet_list.append(Bullet(self.player.center_x, self.player.center_y, world_pos.x, world_pos.y))

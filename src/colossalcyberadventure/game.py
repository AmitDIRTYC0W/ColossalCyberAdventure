from math import floor, ceil
from pathlib import Path
from threading import Thread, Lock

import arcade
from pytiled_parser import parse_world

from arcade import SpriteList, Scene
from pyglet.math import Vec2
import arcade.gui
from arcade import key as k

from src.colossalcyberadventure.bullet import Bullet
from src.colossalcyberadventure.camera import GameCam
from src.colossalcyberadventure.player import Player


class GameView(arcade.View):
    """View of the actual game

    Attributes
    ----------
    player: Player
    keyboard_state: dict[int, bool]
    scene: arcade.scene.Scene
    WORLD_TILEMAP_WIDTH:
        number of tilemaps that together create the width of the world
    """

    BACKGROUND_COLOR = arcade.color.JET
    WORLD_PATH = "resources/map/map.world"
    MAP_PARTIAL_WIDTH = 2560
    MAP_PARTIAL_HEIGHT = 1440
    WORLD_TILEMAP_WIDTH = 30
    WORLD_TILEMAP_HEIGHT = 30

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.bullet_list = SpriteList()
        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False, k.Q: False}
        self.camera = GameCam(self.window.width, self.window.height, self.player)
        self.world = parse_world(Path(GameView.WORLD_PATH))
        # y-x.tmx
        self.scene = arcade.Scene()
        map_world_x, map_world_y = floor(self.player.center_x / GameView.MAP_PARTIAL_WIDTH), floor(
            self.player.center_y / GameView.MAP_PARTIAL_HEIGHT
        )
        self.connect_scenes(self.get_scene_from_partial_tilemap(map_world_x, map_world_y),
                            f"{map_world_x}-{map_world_y}")
        self.maps_in_loading = []

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

    def get_scene_from_partial_tilemap(self, x, y):
        return arcade.Scene.from_tilemap(
            # I know it looks like it should be y * WORLD_TILEMAP_WIDTH + x but IDGAF
            arcade.load_tilemap(self.world.maps[x * GameView.WORLD_TILEMAP_WIDTH + y].map_file, use_spatial_hash=True,
                                offset=Vec2(x * GameView.MAP_PARTIAL_WIDTH, y * GameView.MAP_PARTIAL_HEIGHT)))

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
        map_x = floor(self.player.center_x / GameView.MAP_PARTIAL_WIDTH)
        map_y = floor(self.player.center_y / GameView.MAP_PARTIAL_HEIGHT)
        for y in range(max(0, map_y - 1), min(GameView.WORLD_TILEMAP_HEIGHT - 1, map_y + 2)):
            for x in range(max(0, map_x - 1), min(GameView.WORLD_TILEMAP_WIDTH - 1, map_x + 2)):
                key = f"{map_x + x}-{map_y + y}"
                print("maps in loading:", self.maps_in_loading, "name_mappings keys:", self.scene.name_mapping.keys())
                if not (key in self.maps_in_loading or key in self.scene.name_mapping.keys()):
                    print("starting thread", key)
                    self.maps_in_loading.append(key)
                    t = Thread(target=load_map, args=(self, map_x + x, map_y + y))
                    t.start()
            print("-------------------")

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


writing_to_maps_in_loading_lock = Lock()
loading_map_lock = Lock()


def load_map(view: GameView, x, y):
    key = f"{x}-{y}"
    loading_map_lock.acquire(blocking=True)
    view.connect_scenes(view.get_scene_from_partial_tilemap(x, y), key)
    loading_map_lock.release()

    writing_to_maps_in_loading_lock.acquire(blocking=True)
    view.maps_in_loading.remove(key)
    writing_to_maps_in_loading_lock.release()

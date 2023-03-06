from math import floor
from pathlib import Path
import multiprocessing as mp

import _queue
import arcade
from pytiled_parser import parse_world, World

from arcade import SpriteList, Scene
from pyglet.math import Vec2
import arcade.gui
from arcade import key as k

from src.colossalcyberadventure.bullet import Bullet
from src.colossalcyberadventure.camera import GameCam
from src.colossalcyberadventure.player import Player


class TilemapLoader:
    def __init__(self):
        self.queue_in = mp.Queue()
        self.queue_out = mp.Queue()
        self.process = mp.Process(
            target=self.load_maps,
            args=(self.queue_in, self.queue_out),
            daemon=True,
        )

    def load_maps(self, queue_out: mp.Queue):
        while True:
            params = self.queue_in.get(block=True)
            map_loaded = get_scene_from_world(params["x"], params["y"], params["world"],
                                              params["world_width_in_tilemaps"], params["width_px"],
                                              params["height_px"])
            queue_out.put({"scene": map_loaded, "x": params["x"], "y": params["y"]}, block=False)

    def start(self):
        self.process.start()

    def stop(self):
        self.process.terminate()


def load_tilemap(path: str):
    return arcade.load_tilemap(
        path,
        use_spatial_hash=True,
        lazy=True,
    )


def get_scene_from_world(x, y, world: World, world_width_in_tilemaps, tilemap_width_px, tilemap_height_px):
    return arcade.Scene.from_tilemap(
        arcade.load_tilemap(world.maps[x * world_width_in_tilemaps + y].map_file, use_spatial_hash=True,
                            offset=Vec2(x * tilemap_width_px, y * tilemap_height_px))
    )


class GameView(arcade.View):
    """View of the actual game

    Attributes
    ----------
    player: Player
    keyboard_state: dict[int, bool]
    scene: arcade.scene.Scene
    WORLD_WIDTH_TILEMAPS:
        number of tilemaps that together create the width of the world
    """

    BACKGROUND_COLOR = arcade.color.JET
    WORLD_PATH = "resources/map/map.world"
    TILEMAP_WIDTH_PX = 2560
    TILEMAP_HEIGHT_PX = 1440
    WORLD_WIDTH_TILEMAPS = 30
    WORLD_HEIGHT_TILEMAPS = 30

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.bullet_list = SpriteList()
        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False, k.Q: False}
        self.camera = GameCam(self.window.width, self.window.height, self.player)
        self.world = parse_world(Path(GameView.WORLD_PATH))
        # y-x.tmx
        self.scene = arcade.Scene()
        self.non_drawn_scene = arcade.Scene()
        map_world_x, map_world_y = floor(self.player.center_x / GameView.TILEMAP_WIDTH_PX), floor(
            self.player.center_y / GameView.TILEMAP_HEIGHT_PX
        )
        self.connect_scenes(get_scene_from_world(map_world_x, map_world_y, self.world, GameView.WORLD_WIDTH_TILEMAPS,
                                                 GameView.TILEMAP_WIDTH_PX, GameView.TILEMAP_HEIGHT_PX),
                            f"{map_world_x}-{map_world_y}")
        self.loader = TilemapLoader()
        self.loader_started = False
        self.maps_in_loading = []

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

    def get_tilemap_file_from_world(self, x, y):
        return self.world.maps[x * GameView.WORLD_WIDTH_TILEMAPS + y].map_file

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
        if not self.loader_started:
            self.loader.start()
            self.loader_started = True
        map_x = floor(self.player.center_x / GameView.TILEMAP_WIDTH_PX)
        map_y = floor(self.player.center_y / GameView.TILEMAP_HEIGHT_PX)
        for y in range(max(0, map_y - 1), min(GameView.WORLD_HEIGHT_TILEMAPS - 1, map_y + 2)):
            for x in range(max(0, map_x - 1), min(GameView.WORLD_WIDTH_TILEMAPS - 1, map_x + 2)):
                key = f"{map_x + x}-{map_y + y}"
                if not (key in self.maps_in_loading or key in self.scene.name_mapping.keys()):
                    self.maps_in_loading.append(key)
                    params = {"x": map_x + x, "y": map_y + y, "world": self.world,
                              "world_width_in_tilemaps": GameView.WORLD_WIDTH_TILEMAPS,
                              "width_px": GameView.TILEMAP_WIDTH_PX, "height_px": GameView.TILEMAP_HEIGHT_PX}
                    self.loader.queue_in.put(params)

        if not len(self.maps_in_loading) == 0:
            try:
                return_dict = self.loader.queue_out.get(block=False)
                scene: arcade.Scene = return_dict["scene"]
                x = return_dict["x"]
                y = return_dict["y"]
                self.connect_scenes(scene, f"{x}-{y}")
                self.maps_in_loading.remove(f"{x}-{y}")
            except _queue.Empty:
                pass

        if self.keyboard_state[k.Q]:
            self.loader.stop()
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

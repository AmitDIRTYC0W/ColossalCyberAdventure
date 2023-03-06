import multiprocessing as mp
import random
from math import floor
from pathlib import Path

import _queue
import arcade
import arcade.gui
import arcade.gui
from arcade import Scene
from arcade import SpriteList
from arcade import key as k
from pyglet.math import Vec2
from pytiled_parser import parse_world, World

from constants import *
from src.colossalcyberadventure.camera import GameCam
from src.colossalcyberadventure.enemies import Archer
from src.colossalcyberadventure.enemies import Skeleton
from src.colossalcyberadventure.item import Coin
from src.colossalcyberadventure.item import HealthShroom
from src.colossalcyberadventure.player import Player
from src.colossalcyberadventure.projectile import Projectile
from src.colossalcyberadventure.weapon import AWeapon


class TilemapLoader:
    def __init__(self):
        self.queue_in = mp.Queue()
        self.queue_out = mp.Queue()
        self.process = mp.Process(
            target=self.load_maps,
            args=(self.queue_out,),
            daemon=True,
        )

    def load_maps(self, queue_out: mp.Queue):
        while True:
            params = self.queue_in.get(block=True)
            map_loaded = tilemap_from_world(params["x"], params["y"], params["world"],
                                            params["world_width_in_tilemaps"], params["width_px"], params["height_px"])
            queue_out.put({"tilemap": map_loaded, "x": params["x"], "y": params["y"]}, block=False)

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


def tilemap_from_world(x, y, world: World, world_width_in_tilemaps, tilemap_width_px, tilemap_height_px):
    return arcade.load_tilemap(world.maps[x * world_width_in_tilemaps + y].map_file, layer_options={
        "water": {
            "use_spatial_hash": True,
        },
        "obstacles": {
            "use_spatial_hash": True,
        }
    }, offset=Vec2(x * tilemap_width_px, y * tilemap_height_px), scaling=TILE_SCALING)


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
    SKELETON_AMOUNT = 10
    ARCHER_AMOUNT = 5
    SLIME_AMOUNT = 0
    COIN_AMOUNT = 1000
    HEALTH_SHROOM_AMOUNT = 10
    WORLD_PATH = "resources/map/map.world"
    TILEMAP_WIDTH_PX = 1920
    TILEMAP_HEIGHT_PX = 1080
    WORLD_WIDTH_TILEMAPS = 40
    WORLD_HEIGHT_TILEMAPS = 40

    def __init__(self):
        super().__init__()

        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False, k.C: False, k.H: False, k.Q: False,
                               k.I: False}
        self.player_projectile_list = SpriteList(use_spatial_hash=True)
        self.enemy_projectile_list = SpriteList(use_spatial_hash=True)
        self.inventory_state = False
        self.player_projectile_list = SpriteList()
        self.enemy_projectile_list = SpriteList()
        self.item_array = arcade.SpriteList()

        for i in range(GameView.COIN_AMOUNT):
            x = random.randrange(MAP_WIDTH)
            y = random.randrange(MAP_HEIGHT)
            coin = Coin(x, y)
            self.item_array.append(coin)
        for i in range(GameView.HEALTH_SHROOM_AMOUNT):
            x = random.randrange(MAP_WIDTH)
            y = random.randrange(MAP_HEIGHT)
            healthshroom = HealthShroom(x, y)
            self.item_array.append(healthshroom)
        self.scene = arcade.Scene()
        self.player = Player(self.enemy_projectile_list, self.player_projectile_list, self.item_array,
                             self.keyboard_state, self.scene)
        #
        self.enemy_array = SpriteList(use_spatial_hash=True)
        for i in range(GameView.SKELETON_AMOUNT):
            self.enemy_array.append(Skeleton(self.player, self.enemy_array,
                                             self.enemy_projectile_list, self.player_projectile_list))
        for i in range(GameView.ARCHER_AMOUNT):
            self.enemy_array.append(Archer(self.player, self.enemy_array,
                                           self.enemy_projectile_list, self.player_projectile_list))
        self.weapon = AWeapon(self.player)

        self.camera = GameCam(self.player)
        self.world = parse_world(Path(GameView.WORLD_PATH))
        self.non_drawn_scene = arcade.Scene()
        map_world_x, map_world_y = floor(self.player.center_x / GameView.TILEMAP_WIDTH_PX), floor(
            self.player.center_y / GameView.TILEMAP_HEIGHT_PX
        )
        self.connect_scenes(arcade.Scene.from_tilemap(
            tilemap_from_world(map_world_x, map_world_y, self.world, GameView.WORLD_WIDTH_TILEMAPS,
                               GameView.TILEMAP_WIDTH_PX, GameView.TILEMAP_HEIGHT_PX)), "0-0")
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

    def get_enemy_array(self):
        return self.enemy_array

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()
        self.player.draw()
        self.enemy_array.draw()
        self.player_projectile_list.draw()
        self.enemy_projectile_list.draw()
        self.weapon.draw()
        self.item_array.draw()
        if self.inventory_state:
            self.player.inventory.draw()

    def on_update(self, delta_time: float):
        self.player.update_player_speed(self.keyboard_state, self.enemy_array)
        self.enemy_array.update()
        if not self.loader_started:
            self.loader.start()
            self.loader_started = True

        map_x = floor(self.player.center_x / GameView.TILEMAP_WIDTH_PX)
        map_y = floor(self.player.center_y / GameView.TILEMAP_HEIGHT_PX)
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if not (map_x + x_offset < 0 or map_x + x_offset >= 40) and not (
                        map_y + y_offset < 0 or map_y + y_offset >= 40) and not (x_offset == 0 and y_offset == 0):
                    key = f"{map_x + x_offset}-{map_y + y_offset}"
                    if not (key in self.maps_in_loading or key in self.scene.name_mapping.keys()):
                        self.maps_in_loading.append(key)
                        params = {"x": map_x + x_offset, "y": map_y + y_offset, "world": self.world,
                                  "world_width_in_tilemaps": GameView.WORLD_WIDTH_TILEMAPS,
                                  "width_px": GameView.TILEMAP_WIDTH_PX, "height_px": GameView.TILEMAP_HEIGHT_PX}
                        self.loader.queue_in.put(params)

        if not len(self.maps_in_loading) == 0:
            try:
                return_dict = self.loader.queue_out.get(block=False)
                tilemap = return_dict["tilemap"]
                x_offset = return_dict["x"]
                y_offset = return_dict["y"]
                self.connect_scenes(arcade.Scene.from_tilemap(tilemap), f"{x_offset}-{y_offset}")
                self.maps_in_loading.remove(f"{x_offset}-{y_offset}")
            except _queue.Empty:
                pass

        if self.keyboard_state[k.Q]:
            self.loader.stop()
            quit()
        self.player.update_player_speed(self.keyboard_state, self.enemy_array)
        self.player.update_animation()
        self.enemy_array.update_animation()
        self.player.update()
        self.camera.center_camera_on_player()
        self.player_projectile_list.update()
        self.enemy_projectile_list.update()
        self.weapon.update()
        self.player.inventory.update(self.camera.position.x, self.camera.position.y)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = True
        if symbol == arcade.key.I:
            self.inventory_state = not self.inventory_state

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        world_pos = self.mouse_to_world_position(x, y)
        if self.inventory_state:
            return

        else:
            bullet_path = "resources/bullet/0.png"
            self.player_projectile_list.append(Projectile(
                self.weapon.center_x, self.weapon.center_y, world_pos.x, world_pos.y, bullet_path, 1))

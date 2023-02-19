import arcade

from arcade import SpriteList
from pyglet.math import Vec2
import arcade.gui
from arcade import key as k

from src.colossalcyberadventure.projectile import Projectile
from src.colossalcyberadventure.camera import GameCam
from src.colossalcyberadventure.player import Player
from src.colossalcyberadventure.enemies import Skeleton
from src.colossalcyberadventure.enemies import Archer
from src.colossalcyberadventure.enemies import Slime
from constants import *


class GameView(arcade.View):
    """View of the actual game

    Attributes
    ----------
    player: Player
    keyboard_state: dict[int, bool]
    map: arcade.tile-map.TileMap
        The full map
    scene: arcade.scene.Scene
    """

    BACKGROUND_COLOR = arcade.color.JET
    MAP_PATH = "resources/map/map.tmj"
    SKELETON_AMOUNT = 15
    ARCHER_AMOUNT = 5
    SLIME_AMOUNT = 5

    def __init__(self):
        super().__init__()

        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False, k.C: False}
        self.player_projectile_list = SpriteList()
        self.enemy_projectile_list = SpriteList()
        self.player = Player(self.enemy_projectile_list, self.player_projectile_list, self.keyboard_state)
        #
        self.enemy_array = SpriteList(use_spatial_hash=True)
        for i in range(GameView.SKELETON_AMOUNT):
            self.enemy_array.append(Skeleton(self.player, self.enemy_array,
                                             self.enemy_projectile_list, self.player_projectile_list))
        for i in range(GameView.ARCHER_AMOUNT):
            self.enemy_array.append(Archer(self.player, self.enemy_array,
                                           self.enemy_projectile_list, self.player_projectile_list))
        for i in range(GameView.SLIME_AMOUNT):
            self.enemy_array.append(Slime(
                self.player, self.enemy_array, self.enemy_projectile_list, self.player_projectile_list))
        #
        self.camera = GameCam(self.window.width, self.window.height, self.player)
        self.map = arcade.load_tilemap(GameView.MAP_PATH, TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.map)

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

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
        self.enemy_array.draw()
        self.player_projectile_list.draw()
        self.enemy_projectile_list.draw()

    def on_update(self, delta_time: float):
        self.player.update_player_speed(self.keyboard_state)
        self.enemy_array.update()
        self.player.update_animation()
        self.enemy_array.update_animation()
        self.player.update()
        self.camera.center_camera_on_player()
        self.player_projectile_list.update()
        self.enemy_projectile_list.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = True

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        BULLET_PATH = "resources/bullet/0.png"
        world_pos = self.mouse_to_world_position(x, y)
        self.player_projectile_list.append(Projectile(
            self.player.center_x, self.player.center_y, world_pos.x, world_pos.y, BULLET_PATH, 1))

import random

import arcade

from arcade import SpriteList
from pyglet.math import Vec2
import arcade.gui
from arcade import key as k

from src.colossalcyberadventure.weapon import AWeapon
from src.colossalcyberadventure.projectile import Projectile
from src.colossalcyberadventure.camera import GameCam
from src.colossalcyberadventure.player import Player
from src.colossalcyberadventure.enemies import Skeleton
from src.colossalcyberadventure.enemies import Archer
from constants import *
import constants


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
    ARCHER_AMOUNT = 0
    SLIME_AMOUNT = 0

    def __init__(self):
        super().__init__()

        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False, k.C: False, k.H: False}
        self.player_projectile_list = SpriteList(use_spatial_hash=True)
        self.enemy_projectile_list = SpriteList(use_spatial_hash=True)
        self.inventory_state = False
        self.bot_on = False
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
        self.weapon = AWeapon(self.player)

        self.camera = GameCam(self.window.width, self.window.height, self.player)
        constants.SCREEN_WIDTH = self.window.width
        constants.SCREEN_HEIGHT = self.window.height
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
        if self.inventory_state:
            self.player.inventory.draw()
        if self.bot_on:
            self.player.bot()
    def on_update(self, delta_time: float):
        self.player.update_player_speed(self.keyboard_state, self.enemy_array)
        self.enemy_array.update()
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
        if symbol == arcade.key.B:
            self.bot_on = not self.bot_on
    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        world_pos = self.mouse_to_world_position(x, y)
        if self.inventory_state:
            for item_slot in self.player.inventory.grid_sprite_list:
                item_slot.is_touched(world_pos[0], world_pos[1])

        else:
            BULLET_PATH = "resources/bullet/0.png"
            self.player_projectile_list.append(Projectile(
                self.weapon.center_x, self.weapon.center_y, world_pos.x, world_pos.y, BULLET_PATH, 1))

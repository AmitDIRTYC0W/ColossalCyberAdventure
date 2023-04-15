import time
from enum import Enum

import arcade
import arcade.key as k
from arcade import SpriteList
from arcade.hitbox import HitBox
from pyglet.math import Vec2

from .common import check_map_bounds
from .entity import IEntity
from .projectile import Projectile
from .healthbar import HealthBar
from .inventory import Inventory
from .item import Coin
from .item import HealthShroom


class PlayerAnimationState(Enum):
    """Holds the path inside the resources folder and the amount of frames in the animation"""
    IDLE = ("idle", 8)
    WALK = ("walk", 8)


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"


TEXTURES_BASE = {
    PlayerAnimationState.IDLE: {Direction.LEFT: [], Direction.RIGHT: []},
    PlayerAnimationState.WALK: {Direction.LEFT: [], Direction.RIGHT: []}}

textures = TEXTURES_BASE


def load_textures():
    """Load textures into textures dictionary

    This function loads all frames of the animation into the dictionary and also loads
    a flipped version.

    Returns
    -------

    """
    for state in PlayerAnimationState:
        textures[state] = {}
        textures[state][Direction.RIGHT] = []
        textures[state][Direction.LEFT] = []
        for i in range(state.value[1]):
            tex_left, tex_right = arcade.load_texture_pair(f":data:player/{state.value[0]}/{i}.png")
            textures[state][Direction.RIGHT].append(tex_left)
            textures[state][Direction.LEFT].append(tex_right)


class Player(arcade.Sprite, IEntity):
    """Main player class

    loads the textures for the player when initialized. Should only happen once.

    Attributes
    ----------
    _state: PlayerAnimationState
        Should only be changed by the current class
    direction: Direction
        What direction the player is facing
    frame_counter: int
        How many frames the current frame of the animation was in
    current_texture_index: int
        What frame number the animation is in
    """
    SPRITE_SCALE = 2
    SPEED = 250
    SKILL_3_SPEED_CHANGE = 3
    FRAMES_PER_TEXTURE = 5
    ALPHA_CHANGE_ON_SKILL_3 = 100
    XP_PER_LEVEL = 5

    def __init__(self, enemy_projectile_list: SpriteList, player_projectile_list: SpriteList, item_array: SpriteList,
                 keyboard_state: dict[int, bool], scene: arcade.Scene, xp_list: SpriteList):
        super().__init__(scale=Player.SPRITE_SCALE, path_or_texture="resources/player/idle/0.png")
        self.animation_state = PlayerAnimationState.IDLE
        if textures == TEXTURES_BASE:
            load_textures()
        self.real_time = time.localtime()
        self.last_skill_1_use = time.gmtime(0)
        self.last_skill_2_use = time.gmtime(0)
        self.last_skill_3_use = time.gmtime(0)
        self.using_skill_3 = False
        self.keyboard_state = keyboard_state
        self.player_projectile_list = player_projectile_list
        self.enemy_projectile_list = enemy_projectile_list
        self.delta_change_x = 0
        self.delta_change_y = 0
        self.scene = scene
        self._state = PlayerAnimationState.IDLE
        self.direction = Direction.RIGHT
        self.texture = textures[PlayerAnimationState.IDLE][self.direction][0]
        self.frame_counter = 0
        self.current_texture_index = 0
        self.xp = 0
        self.level = 3
        self.xp_list = xp_list
        self.health_bar = HealthBar(self, 70, 5, 1, arcade.color.BLACK, arcade.color.RED)
        self.should_reset_sprite_counter = False
        self.item_array = item_array
        self.coin_counter = 0
        self.health_shroom_counter = 0
        self.inventory = Inventory(
            self.coin_counter,
            self.health_shroom_counter,
            self,
            owner=self,
        )

    def update_state(self, new_state: PlayerAnimationState):
        """Update the player state and reset counters

        Parameters
        ----------
        new_state: PlayerAnimationState

        Returns
        -------

        """
        self._state = new_state
        self.frame_counter = 0
        self.current_texture_index = 0

    def draw(self, *, draw_filter=None, pixelated=None, blend_function=None):
        super().draw(filter=draw_filter, pixelated=pixelated, blend_function=blend_function)
        self.health_bar.draw()

    def update_animation(self, delta_time: float = 1 / 60):

        if self.frame_counter == 0 or self.should_reset_sprite_counter:
            self.frame_counter = 0
            self.current_texture_index += 1
            if self.current_texture_index >= self._state.value[1] or self.should_reset_sprite_counter:
                self.current_texture_index = 0
            self.should_reset_sprite_counter = False
            self.texture = textures[self._state][self.direction][self.current_texture_index]
            self.hit_box = HitBox(
                self.texture.hit_box_points,
                position=self.position,
                scale=self.scale_xy,
            )

        self.frame_counter += 1
        if self.frame_counter > Player.FRAMES_PER_TEXTURE:
            self.frame_counter = 0

    def update_direction(self):
        old_direction = self.direction
        if self.change_x < 0:
            self.direction = Direction.LEFT
        elif self.change_x > 0:
            self.direction = Direction.RIGHT
        #
        if old_direction != self.direction:
            self.should_reset_sprite_counter = True

    def on_update(self, delta_time: float = 1 / 60):
        """Updates player position and checks for collision
        Run this function every update of the window

        """
        if self._state.value[0] != self.animation_state.value[0]:
            self.update_state(self.animation_state)
        self.update_direction()
        # self.center_x += self.change_x
        # self.center_y += self.change_y
        #
        # for projectile in self.enemy_projectile_list:
        #     if arcade.check_for_collision(self, projectile):
        #         self.reduce_health(1)
        #         projectile.remove_from_sprite_lists()
        #
        # check_map_bounds(self)
        #
        # self.health_bar.update()
        # self.real_time = time.localtime()
        #
        # if abs(self.real_time.tm_sec - self.last_skill_3_use.tm_sec) >= 3 and self.using_skill_3:
        #     self.using_skill_3 = False
        #     self.alpha += Player.ALPHA_CHANGE_ON_SKILL_3
        #
        # if self.keyboard_state[k.C]:
        #     self.on_skill_1()
        #
        # if self.keyboard_state[k.H]:
        #     self.on_skill_2()
        #
        # if self.keyboard_state[k.V]:
        #     self.on_skill_3()
        #
        # self.check_collision_with_items()

    def get_state(self):
        return self._state

    def get_direction(self):
        return self.direction

    def get_position(self) -> tuple[float, float]:  # TODO send Goni everything
        """Returns the player position relative to the map in px

        See Also
        --------
        src.colossalcyberadventure.game.ColossalCyberAdventure: main window class

        Returns
        -------
        int
            x value of player's center (in pixels)
        int
            y value of player's center (in pixels)
        """
        return self.center_x, self.center_y

    def update_player_speed(self, keyboard_state: dict[int, bool], enemy_array, delta_time):
        """Updates player change_x and change_y values and the player state

        Changes these values in accordance to the currently pressed keys.
        Change the state to walking if the player is moving idle if not.
        """
        movement_vec = Vec2(0, 0)

        if keyboard_state[k.A] or keyboard_state[k.D]:
            new_state = PlayerAnimationState.WALK
        else:
            new_state = PlayerAnimationState.IDLE

        if new_state != self._state:
            self.update_state(new_state)

        if keyboard_state[k.W] and not keyboard_state[k.S]:
            movement_vec.y = 1
        elif keyboard_state[k.S] and not keyboard_state[k.W]:
            movement_vec.y = -1
        if keyboard_state[k.A] and not keyboard_state[k.D]:
            movement_vec.x = -1
        elif keyboard_state[k.D] and not keyboard_state[k.A]:
            movement_vec.x = 1

        if self.using_skill_3:
            movement_vec = movement_vec.normalize() * (Player.SPEED + Player.SKILL_3_SPEED_CHANGE)
        else:
            movement_vec = movement_vec.normalize() * Player.SPEED
        movement_vec = movement_vec * delta_time
        self.change_x = movement_vec.x
        self.change_y = movement_vec.y
        self.center_x += self.change_x
        self.center_y += self.change_y

        enemy_collisions = arcade.check_for_collision_with_list(self, enemy_array)

        if len(enemy_collisions) >= 1:
            self.reduce_health(0.2)
            self.center_x -= self.change_x
            self.center_y -= self.change_y
            self.change_x = 0
            self.change_y = 0
        self.center_x -= self.change_x
        self.center_y -= self.change_y

    def on_skill_1(self):
        projectile_path = ":data:bullet/0.png"
        if abs(self.real_time.tm_sec - self.last_skill_1_use.tm_sec) >= 2 and self.level >= 2:
            directions = [
                [self.center_x, self.center_y + 1], [self.center_x + 1, self.center_y + 1],
                [self.center_x + 1, self.center_y], [self.center_x + 1, self.center_y - 1],
                [self.center_x, self.center_y - 1], [self.center_x - 1, self.center_y - 1],
                [self.center_x - 1, self.center_y], [self.center_x - 1, self.center_y + 1]
            ]

            for i in range(8):
                self.player_projectile_list.append(
                    Projectile(self.center_x, self.center_y, directions[i][0], directions[i][1], projectile_path, 2))
            self.last_skill_1_use = self.real_time

    def on_skill_2(self):
        if abs(self.real_time.tm_sec - self.last_skill_2_use.tm_sec) >= 5 and self.level >= 2:
            if self.health_bar.health_points <= 80:
                self.health_bar.health_points += 20
            elif self.health_bar.health_points <= 100:
                self.health_bar.health_points = 100
            else:
                return
            self.last_skill_2_use = self.real_time

    def on_skill_3(self):
        if abs(self.real_time.tm_sec - self.last_skill_3_use.tm_sec) >= 7 and self.level >= 3:
            self.using_skill_3 = True
            self.last_skill_3_use = self.real_time
            self.alpha -= Player.ALPHA_CHANGE_ON_SKILL_3

    def reduce_health(self, amount):
        if self.health_bar.health_points > 0:
            self.health_bar.health_points -= amount
            self.last_skill_3_use = self.real_time

    def check_collision_with_items(self):
        item_collided_list = arcade.check_for_collision_with_list(self, self.item_array)
        for item in item_collided_list:
            if isinstance(item, Coin):
                self.coin_counter += 1
            if isinstance(item, HealthShroom):
                self.health_shroom_counter += 1
            item.remove_from_sprite_lists()

        xp_collision_list = arcade.check_for_collision_with_list(self, self.xp_list)
        for xp in xp_collision_list:
            self.xp += 1
            self.level = self.xp // Player.XP_PER_LEVEL + 1
            xp.remove_from_sprite_lists()

    def get_item_counter(self):
        return self.coin_counter, self.health_shroom_counter

    def check_death(self):
        if self.health_bar.health_points <= 0:
            return True


class AdditionRequest:
    def __init__(self, addition_type):
        self.type = addition_type

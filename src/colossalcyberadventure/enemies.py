from enum import Enum
import random

from arcade import SpriteList
from pyglet.math import Vec2

from entity import IEntity
from constants import *

from src.colossalcyberadventure.player import Player
import arcade


class EnemyAnimationState(Enum):
    """Holds the path inside the resources folder and the amount of frames in the animation"""
    IDLE = ("idle", 1)
    WALK = ("walk", 4)


class Direction(Enum):
    DOWN = "down"
    UP = "up"
    LEFT = "left"
    RIGHT = "right"


TEXTURES_BASE = {
    EnemyAnimationState.IDLE: {Direction.LEFT: [], Direction.RIGHT: [], Direction.UP: [], Direction.DOWN: []},
    EnemyAnimationState.WALK: {Direction.LEFT: [], Direction.RIGHT: [], Direction.UP: [], Direction.DOWN: []}}

textures = TEXTURES_BASE


def load_textures():
    """Load textures into textures dictionary

    This function loads all frames of the animation into the dictionary and also loads
    a flipped version.

    Returns
    -------

    """
    for direction in Direction:
        for state in EnemyAnimationState:
            for i in range(state.value[1]):
                tex = arcade.load_texture(f"resources/enemies/slime/{direction.value}/{state.value[0]}/{i}.png")
                textures[state][direction].append(tex)


class Enemy(arcade.Sprite, IEntity):
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

    SPRITE_SCALE = 3

    SPEED = 3
    FRAMES_PER_TEXTURE = 10

    def __init__(self, player: Player, enemy_array: SpriteList):
        super().__init__(scale=Enemy.SPRITE_SCALE)
        if textures == TEXTURES_BASE:
            load_textures()
        self.player = player
        self.enemy_array = enemy_array

        self.center_x = random.randint(0, MAP_WIDTH)
        self.center_y = random.randint(0, MAP_HEIGHT)
        self.delta_change_x = 0
        self.delta_change_y = 0
        self._state = EnemyAnimationState.WALK
        self.direction = Direction.DOWN
        self.texture = textures[EnemyAnimationState.IDLE][self.direction][0]
        self.frame_counter = 0
        self.current_texture_index = 0
        # self.health_bar = HealthBar(self, 70, 5, 1, arcade.color.BLACK, arcade.color.RED)

    def update_state(self, new_state: EnemyAnimationState):
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
        # self.health_bar.draw()

    def update_animation(self, delta_time: float = 1 / 60):
        self.frame_counter += 1
        if self.frame_counter > Enemy.FRAMES_PER_TEXTURE:
            self.current_texture_index += 1
            if self.current_texture_index >= self._state.value[1]:
                self.current_texture_index = 0
            self.texture = textures[self._state][self.direction][self.current_texture_index]
            self.frame_counter = 0

    def update(self):
        """Updates player position and checks for collision
        Run this function every update of the window

        """

        self.update_enemy_speed()

        self.center_x += self.change_x
        self.center_y += self.change_y

        enemy_collisions = arcade.check_for_collision_with_list(self, self.enemy_array)
        if len(enemy_collisions) >= 1:
            self.center_x -= self.change_x
            self.center_y -= self.change_y

        if self.change_x != 0 or self.change_y != 0:
            self._state = EnemyAnimationState.WALK
        else:
            self._state = EnemyAnimationState.IDLE

        if self.change_y < 0:
            if self.change_x < 0:
                if abs(self.change_x) > abs(self.change_y):
                    self.direction = Direction.LEFT
                else:
                    self.direction = Direction.DOWN
            else:
                if abs(self.change_x) > abs(self.change_y):
                    self.direction = Direction.RIGHT
                else:
                    self.direction = Direction.DOWN

        if self.change_y > 0:
            if self.change_x < 0:
                if abs(self.change_x) > abs(self.change_y):
                    self.direction = Direction.LEFT
                else:
                    self.direction = Direction.UP
            else:
                if abs(self.change_x) > abs(self.change_y):
                    self.direction = Direction.RIGHT
                else:
                    self.direction = Direction.UP

        if self.left < 0:
            self.left = 0
        if self.right > MAP_WIDTH - 1:
            self.right = MAP_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        if self.top > MAP_HEIGHT - 1:
            self.top = MAP_HEIGHT - 1

        # if arcade.check_for_collision(self.player, self):

        #     self.health_bar.update()

    def get_position(self) -> tuple[float, float]:
        """Returns the enemy position relative to the map in px

        See Also
        --------
        src.colossalcyberadventure.game.ColossalCyberAdventure: main window class

        Returns
        -------
        int
            x value of enemy's center (in pixels)
        int
            y value of enemy's center (in pixels)
        """
        return self.center_x, self.center_y

    def update_enemy_speed(self):
        """Updates player change_x and change_y values and the player state

        Changes these values in accordance to the currently pressed keys.
        Change the state to walking if the player is moving idle if not.
        """

        target_x = self.player.center_x
        target_y = self.player.center_y
        origin_x, origin_y = self.get_position()

        self.center_x = origin_x
        self.center_y = origin_y
        direction = Vec2(target_x - origin_x, target_y - origin_y).normalize() * Vec2(Enemy.SPEED, Enemy.SPEED)
        self.change_x = direction.x
        self.change_y = direction.y

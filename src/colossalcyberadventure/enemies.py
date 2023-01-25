from enum import Enum
from math import atan2, degrees

from pyglet.math import Vec2


from entity import IEntity
from constants import *

from src.colossalcyberadventure.player import Player
from src.colossalcyberadventure.healthbar import HealthBar
import arcade


# class EnemyAnimationState(Enum):
#     """Holds the path inside the resources folder and the amount of frames in the animation"""
#     IDLE = ("idle", 1)
#     WALK = ("walk", 8)
#
#
# class Direction(Enum):
#     DOWN = "down"
#     UP = "up"
#     LEFT = "left"
#     RIGHT = "right"
#
#
# TEXTURES_BASE = {
#     PlayerAnimationState.IDLE: {Direction.LEFT: [], Direction.RIGHT: [], Direction.UP: [], Direction.DOWN: []},
#     PlayerAnimationState.WALK: {Direction.LEFT: [], Direction.RIGHT: [], Direction.UP: [], Direction.DOWN: []}}
#
# textures = TEXTURES_BASE
#

def load_textures():
    """Load textures into textures dictionary

    This function loads all frames of the animation into the dictionary and also loads
    a flipped version.

    Returns
    -------

    """
    # for direction in Direction:
    #     for state in PlayerAnimationState:
    #         for i in range(state.value[1]):
    #             tex = arcade.load_texture(f"resources/player/{direction.value}/{state.value[0]}/{i}.png")
    #             textures[state][direction].append(tex)


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
    FRAMES_PER_TEXTURE = 5

    def __init__(self, player: Player):
        super().__init__(scale=Enemy.SPRITE_SCALE)
        # if textures == TEXTURES_BASE:
        #     load_textures()
        self.player = player
        self.center_x = MAP_WIDTH // 2 + 100
        self.center_y = MAP_HEIGHT // 2
        self.delta_change_x = 0
        self.delta_change_y = 0
        # self._state = PlayerAnimationState.IDLE
        # self.direction = Direction.DOWN
        # self.texture = textures[PlayerAnimationState.IDLE][self.direction][0]
        self.texture = arcade.load_texture(f"resources/enemy/Ide1.png")
        # self.frame_counter = 0
        # self.current_texture_index = 0
        # self.health_bar = HealthBar(self, 70, 5, 1, arcade.color.BLACK, arcade.color.RED)

    # def update_state(self, new_state: PlayerAnimationState):
    #     """Update the player state and reset counters
    #
    #     Parameters
    #     ----------
    #     new_state: PlayerAnimationState
    #
    #     Returns
    #     -------
    #
    #     """
    #     self._state = new_state
    #     self.frame_counter = 0
    #     self.current_texture_index = 0

    def draw(self, *, draw_filter=None, pixelated=None, blend_function=None):
        super().draw(filter=draw_filter, pixelated=pixelated, blend_function=blend_function)
        # self.health_bar.draw()

    # def update_animation(self, delta_time: float = 1 / 60):
    #     self.frame_counter += 1
    #     if self.frame_counter > Player.FRAMES_PER_TEXTURE:
    #         self.current_texture_index += 1
    #         if self.current_texture_index >= self._state.value[1]:
    #             self.current_texture_index = 0
    #         self.texture = textures[self._state][self.direction][self.current_texture_index]
    #         self.frame_counter = 0

    def update(self):
        """Updates player position and checks for collision
        Run this function every update of the window

        """
        self.center_x += self.change_x
        self.center_y += self.change_y

    #
    #     if self.change_y < 0:
    #         self.direction = Direction.DOWN
    #     elif self.change_y > 0:
    #         self.direction = Direction.UP
    #
    #     if self.change_x < 0:
    #         self.direction = Direction.LEFT
    #     elif self.change_x > 0:
    #         self.direction = Direction.RIGHT
    #
    #     if self.left < 0:
    #         self.left = 0
    #     if self.right > MAP_WIDTH - 1:
    #         self.right = MAP_WIDTH - 1
    #
    #     if self.bottom < 0:
    #         self.bottom = 0
    #     if self.top > MAP_HEIGHT - 1:
    #         self.top = MAP_HEIGHT - 1
    #
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

from enum import Enum

from pyglet.math import Vec2

from entity import IEntity
from constants import *
import arcade


class PlayerState(Enum):
    """holds the path inside the resources folder and the amount of frames in the animation"""
    IDLE = ("idle", 8)
    WALK = ("walk", 8)


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"


textures = {PlayerState.IDLE: {Direction.LEFT: [], Direction.RIGHT: []},
            PlayerState.WALK: {Direction.LEFT: [], Direction.RIGHT: []}}


def load_textures():
    """Load textures into textures dictionary

    This function loads all frames of the animation into the dictionary and also loads
    a flipped version.

    Returns
    -------

    """
    for state in PlayerState:
        for i in range(state.value[1]):
            left, right = arcade.texture.load_texture_pair(f"resources/player/{state.value[0]}/{i}.png")
            textures[state][Direction.LEFT].append(left)
            textures[state][Direction.RIGHT].append(right)


class Player(arcade.Sprite, IEntity):
    """Main player class

    loads the textures for the player when initialized. Should only happen once.

    Attributes
    ----------
    _state: PlayerState
        Should only be changed by the current class
    direction: Direction
        What direction the player is facing
    frame_counter: int
        How many frames the current frame of the animation was in
    current_texture_index: int
        What frame number the animation is in
    """
    SPEED = 7
    FRAMES_PER_TEXTURE = 5

    def __init__(self):
        super().__init__()
        if textures == {PlayerState.IDLE: {Direction.LEFT: [], Direction.RIGHT: []},
                        PlayerState.WALK: {Direction.LEFT: [], Direction.RIGHT: []}}:
            load_textures()
        self.center_x = MAP_WIDTH // 2
        self.center_y = MAP_HEIGHT // 2
        self._state = PlayerState.IDLE
        self.direction = Direction.LEFT
        self.texture = textures[PlayerState.IDLE][self.direction][0]
        self.frame_counter = 0
        self.current_texture_index = 0

    def update_state(self, new_state: PlayerState):
        """Update the player state and reset counters

        Parameters
        ----------
        new_state: PlayerState

        Returns
        -------

        """
        self._state = new_state
        self.frame_counter = 0
        self.current_texture_index = 0

    def update_animation(self, delta_time: float = 1 / 60):
        self.frame_counter += 1
        if self.frame_counter > Player.FRAMES_PER_TEXTURE:
            self.current_texture_index += 1
            if self.current_texture_index >= self._state.value[1]:
                self.current_texture_index = 0
            self.texture = textures[self._state][self.direction][self.current_texture_index]
            self.frame_counter = 0

    def update(self):
        """ Updates player position and checks for collision
        Run this function every update of the window

        """
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x < 0:
            self.direction = Direction.RIGHT
        elif self.change_x > 0:
            self.direction = Direction.LEFT

        if self.left < 0:
            self.left = 0
        if self.right > MAP_WIDTH - 1:
            self.right = MAP_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        if self.top > MAP_HEIGHT - 1:
            self.top = MAP_HEIGHT - 1

    def get_position(self) -> tuple[float, float]:
        """Returns the player position relative to the map

        See Also
        --------
        colossalcyberadventure.game: main window class

        Returns
        -------
        int
            x value of player's center (in pixels)
        int
            y value of player's center (in pixels)
        """

        return self.center_x, self.center_y

    def update_player_speed(self, keyboard_state: dict[int, bool]):
        """Updates player change_x and change_y values and the player state

        Changes these values in accordance to the currently pressed keys.
        Change the state to walking if the player is moving idle if not.
        """
        movement_vec = Vec2(0, 0)

        if True in keyboard_state.values():
            new_state = PlayerState.WALK
        else:
            new_state = PlayerState.IDLE

        if new_state != self._state:
            self.update_state(new_state)

        if keyboard_state[arcade.key.W] and not keyboard_state[arcade.key.S]:
            movement_vec.y = 1
        elif keyboard_state[arcade.key.S] and not keyboard_state[arcade.key.W]:
            movement_vec.y = -1
        if keyboard_state[arcade.key.A] and not keyboard_state[arcade.key.D]:
            movement_vec.x = -1
        elif keyboard_state[arcade.key.D] and not keyboard_state[arcade.key.A]:
            movement_vec.x = 1

        movement_vec = movement_vec.normalize() * Vec2(Player.SPEED, Player.SPEED)
        self.change_x = movement_vec.x
        self.change_y = movement_vec.y
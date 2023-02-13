from enum import Enum
import random
from math import sqrt

from arcade import SpriteList
from pyglet.math import Vec2

from entity import IEntity
from constants import *

from src.colossalcyberadventure.player import Player
import arcade


class SkeletonAnimationState(Enum):
    """Holds the path inside the resources folder and the amount of frames in the animation"""
    IDLE = ("idle", 4)
    WALK = ("walk", 12)


class ArcherAnimationState(Enum):
    """Holds the path inside the resources folder and the amount of frames in the animation"""
    IDLE = ("idle", 4)
    WALK = ("walk", 8)


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"


SKELETON_TEXTURES_BASE = {
    SkeletonAnimationState.IDLE: {Direction.LEFT: [], Direction.RIGHT: []},
    SkeletonAnimationState.WALK: {Direction.LEFT: [], Direction.RIGHT: []}}

skeleton_textures = SKELETON_TEXTURES_BASE

ARCHER_TEXTURES_BASE = {
    SkeletonAnimationState.IDLE: {Direction.LEFT: [], Direction.RIGHT: []},
    SkeletonAnimationState.WALK: {Direction.LEFT: [], Direction.RIGHT: []}}

archer_textures = ARCHER_TEXTURES_BASE


def load_textures(base_path: str, state_enum) -> dict:
    """Load textures into textures dictionary

    This function loads all frames of the animation into the dictionary and also loads
    a flipped version.

    Parameters
    ----------
    base_path: str
        base path to resources directory
    state_enum:
        Enum that contains the information about the sprites.
        For an example see SlimeAnimationState.

    Returns
    -------

    """
    textures = {}

    for state in state_enum:
        textures[state] = {}
        textures[state][Direction.LEFT] = []
        textures[state][Direction.RIGHT] = []
        for i in range(state.value[1]):
            tex_left, tex_right = arcade.load_texture_pair(f"{base_path}/{state.value[0]}/{i}.png")
            textures[state][Direction.LEFT].append(tex_left)
            textures[state][Direction.RIGHT].append(tex_right)

    return textures


class AEnemy(arcade.Sprite, IEntity):

    def __init__(self, player: Player, enemy_array: SpriteList, speed: float, frames_per_texture: int, initial_state,
                 initial_direction: Direction, animation_state,
                 sprite_scale=1.0):
        super().__init__(scale=sprite_scale)

        self.animation_state = animation_state
        self.player = player
        self.enemy_array = enemy_array
        self.speed = speed
        self.frame_counter = 0
        self.frames_per_texture = frames_per_texture
        self.current_texture_index = 0
        self._state = initial_state
        self.direction = initial_direction
        self.textures_array = self.load_textures()
        self.texture = self.textures_array[initial_state][Direction.RIGHT][1]

        collided = True
        while collided:
            self.center_x = random.randint(0, MAP_WIDTH)
            self.center_y = random.randint(0, MAP_HEIGHT)
            self.delta_change_x = 0
            self.delta_change_y = 0
            if len(arcade.check_for_collision_with_list(self, self.enemy_array)) == 0:
                collided = False

    def load_textures(self) -> dict:
        raise NotImplementedError("load_textures() not implemented")

    def update_animation(self, delta_time: float = 1 / 60):
        self.frame_counter += 1
        if self.frame_counter > self.frames_per_texture:
            self.current_texture_index += 1
            if self.current_texture_index >= self._state.value[1]:
                self.current_texture_index = 0
            self.texture = self.textures_array[self._state][self.direction][self.current_texture_index]
            self.frame_counter = 0

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

    def update_state(self, new_state):
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
            self.change_x = 0
            self.change_y = 0

        if self.change_x != 0 or self.change_y != 0:
            self._state = self.animation_state.WALK
        else:
            self._state = self.animation_state.IDLE

        if self.change_x < 0:
            self.direction = Direction.RIGHT
        else:
            self.direction = Direction.LEFT

        if self.left < 0:
            self.left = 0
        if self.right > MAP_WIDTH - 1:
            self.right = MAP_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        if self.top > MAP_HEIGHT - 1:
            self.top = MAP_HEIGHT - 1

        def update_enemy_speed(self):
            """Basic function that walks towards the player by changing the change_x and change_y

            Changes these values in accordance to the location of the player
            """

            target_x = self.player.center_x
            target_y = self.player.center_y
            origin_x, origin_y = self.get_position()

            self.center_x = origin_x
            self.center_y = origin_y
            direction = Vec2(target_x - origin_x, target_y - origin_y).normalize() * Vec2(self.speed, self.speed)
            self.change_x = direction.x
            self.change_y = direction.y


class Skeleton(AEnemy):
    """Slime Class

    loads the textures for the slime when initialized. Should only happen once.

    Attributes
    ----------
    _state: SkeletonAnimationState
        Should only be changed by the current class
    direction: Direction
        What direction the player is facing
    frame_counter: int
        How many frames the current frame of the animation was in
    current_texture_index: int
        What frame number the animation is in
    """

    SPRITE_SCALE = 2
    FRAMES_PER_TEXTURE = 10
    SPEED = 3

    TEXTURES = SKELETON_TEXTURES_BASE

    def __init__(self, player: Player, enemy_array: SpriteList):
        super().__init__(player, enemy_array, Skeleton.SPEED, 5, SkeletonAnimationState.IDLE, Direction.RIGHT, SkeletonAnimationState,
                         Skeleton.SPRITE_SCALE)

    def load_textures(self) -> dict:
        """loads the right textures of the sprite
        """
        if Skeleton.TEXTURES == SKELETON_TEXTURES_BASE:
            textures = load_textures("resources/enemies/skeleton", SkeletonAnimationState)
        else:
            textures = Skeleton.TEXTURES

        return textures

    def update_enemy_speed(self):
        """Updates slimes change_x and change_y

        Changes these values in accordance to the location of the player
        """

        target_x = self.player.center_x
        target_y = self.player.center_y
        origin_x, origin_y = self.get_position()

        self.center_x = origin_x
        self.center_y = origin_y
        direction = Vec2(target_x - origin_x, target_y - origin_y).normalize() * Vec2(self.speed, self.speed)
        self.change_x = direction.x
        self.change_y = direction.y


class Archer(AEnemy):
    """Slime Class

    loads the textures for the slime when initialized. Should only happen once.

    Attributes
    ----------
    _state: SkeletonAnimationState
        Should only be changed by the current class
    direction: Direction
        What direction the player is facing
    frame_counter: int
        How many frames the current frame of the animation was in
    current_texture_index: int
        What frame number the animation is in
    """

    SPRITE_SCALE = 2
    FRAMES_PER_TEXTURE = 10
    SPEED = 4

    TEXTURES = ARCHER_TEXTURES_BASE

    def __init__(self, player: Player, enemy_array: SpriteList):
        super().__init__(player, enemy_array, Archer.SPEED, 5, ArcherAnimationState.IDLE, Direction.RIGHT, ArcherAnimationState,
                         Archer.SPRITE_SCALE)

    def load_textures(self) -> dict:
        """loads the right textures of the sprite
        """
        if Archer.TEXTURES == ARCHER_TEXTURES_BASE:
            textures = load_textures("resources/enemies/archer", ArcherAnimationState)
        else:
            textures = Archer.TEXTURES

        return textures

    def update_enemy_speed(self):
        """Updates slimes change_x and change_y

        Changes these values in accordance to the location of the player
        """
        MIN_DISTANCE_TO_PLAYER = 300
        MAM_DISTANCE_TO_PLAYER = 500

        target_x = self.player.center_x
        target_y = self.player.center_y
        origin_x, origin_y = self.get_position()

        self.center_x = origin_x
        self.center_y = origin_y
        direction = Vec2(target_x - origin_x, target_y - origin_y).normalize() * Vec2(self.speed, self.speed)
        self.change_x = direction.x
        self.change_y = direction.y

        distance_to_player = sqrt(abs(target_x - self.center_x)**2 + abs(target_y - self.center_y)**2)
        if distance_to_player < MIN_DISTANCE_TO_PLAYER:
            self.change_x = -self.change_x
            self.change_y = -self.change_y
        elif distance_to_player < MAM_DISTANCE_TO_PLAYER:
            self.change_x = 0
            self.change_y = 0

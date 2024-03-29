import random
from enum import Enum
from math import sqrt, floor

import arcade
from arcade import SpriteList
from arcade.hitbox import HitBox
from pyglet.math import Vec2

from . import constants
from .entity import IEntity
from .player import Player
from .projectile import Projectile
from .constants import *
from .xp import XP
from .common import check_map_bounds


class SkeletonAnimationState(Enum):
    """Holds the path inside the resources folder and the amount of frames in the animation"""
    IDLE = ("idle", 4)
    WALK = ("walk", 12)
    ATTACK = ("attack", 13)
    DEATH = ("death", 13)


class ArcherAnimationState(Enum):
    """Holds the path inside the resources folder and the amount of frames in the animation"""
    IDLE = ("idle", 4)
    WALK = ("walk", 8)
    ATTACK = ("attack", 7)
    DEATH = ("death", 8)


class SlimeAnimationState(Enum):
    """Holds the path inside the resources folder and the amount of frames in the animation"""
    IDLE = ("idle", 1)
    WALK = ("walk", 4)
    ATTACK = ("attack", 0)
    DEATH = ("death", 0)


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

SLIME_TEXTURES_BASE = {
    SkeletonAnimationState.IDLE: {Direction.LEFT: [], Direction.RIGHT: []},
    SkeletonAnimationState.WALK: {Direction.LEFT: [], Direction.RIGHT: []}}

slime_textures = SKELETON_TEXTURES_BASE


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


# noinspection PyTypeChecker
class AEnemy(arcade.Sprite, IEntity):

    def __init__(self, player: Player, enemy_array: SpriteList, enemy_projectile_list: SpriteList,
                 player_projectile_list: SpriteList, xp_list: SpriteList, speed: float, frames_per_texture: int,
                 initial_state,
                 initial_direction: Direction, animation_state,
                 sprite_scale=1.0,
                 starting_x=random.randint(0, constants.MAP_WIDTH),
                 starting_y=random.randint(0, constants.MAP_HEIGHT),
                 do_start_collision_checking=True):
        super().__init__(scale=sprite_scale)

        self.sprite_scale = sprite_scale
        self.player_projectile_list = player_projectile_list
        self.enemy_projectile_list = enemy_projectile_list
        self.animation_state = animation_state
        self.player = player
        self.enemy_array = enemy_array
        self.xp_list = xp_list
        self.speed = speed
        self.frame_counter = 0
        self.frames_per_texture = frames_per_texture
        self.current_texture_index = 0
        self._state = initial_state
        self.direction = initial_direction
        self.textures_array = self.load_textures()
        self.texture = self.textures_array[initial_state][self.direction][0]
        self.delta_change_x = 0
        self.delta_change_y = 0
        self.center_x = starting_x
        self.center_y = starting_y

        collided = len(arcade.check_for_collision_with_list(self, self.enemy_array)) != 0 or arcade.check_for_collision(
            self, self.player)
        while collided and do_start_collision_checking:
            self.center_x = random.randint(0, constants.MAP_WIDTH)
            self.center_y = random.randint(0, constants.MAP_HEIGHT)
            self.delta_change_x = 0
            self.delta_change_y = 0
            if len(arcade.check_for_collision_with_list(self, self.enemy_array)) == 0 and not \
                    arcade.check_for_collision(self, self.player):
                collided = False
            else:
                self.center_x = random.randint(0, MAP_WIDTH)
                self.center_y = random.randint(0, MAP_HEIGHT)

    def load_textures(self) -> dict:
        raise NotImplementedError("load_textures() not implemented")

    def update_animation(self, delta_time: float = 1 / 60):
        self.frame_counter += 1
        if self.frame_counter > self.frames_per_texture:
            self.current_texture_index += 1
            if self.current_texture_index >= self._state.value[1]:
                self.current_texture_index = 0
            self.texture = self.textures_array[self._state][self.direction][self.current_texture_index]
            self.hit_box = HitBox(
                self.texture.hit_box_points,
                position=self.position,
                scale=self.scale_xy,
            )
            self.frame_counter = 0

    def update_direction(self):
        if self.change_x < 0:
            self.direction = Direction.LEFT
        elif self.change_x > 0:
            self.direction = Direction.RIGHT

    def get_position(self) -> tuple[float, float]:
        """Returns the enemy position relative to the map in px

        See Also
        --------
        colossalcyberadventure.game.ColossalCyberAdventure: main window class

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

    def check_death(self, enemy_to_spawn):
        if self._state != self.animation_state.DEATH:
            for projectile in self.player_projectile_list:
                if arcade.check_for_collision(self, projectile):
                    self._state = self.animation_state.DEATH
                    projectile.remove_from_sprite_lists()
                    self.on_death()

        if self._state == self.animation_state.DEATH:
            self.center_x -= self.change_x
            self.center_y -= self.change_y
            if self.current_texture_index + 1 >= self._state.value[1] and \
                    self.frame_counter + 1 > self.frames_per_texture:
                self.remove_from_sprite_lists()

                self.enemy_array.append(
                    enemy_to_spawn(self.player,
                                   self.enemy_array, self.enemy_projectile_list, self.player_projectile_list,
                                   self.xp_list))

    def on_death(self):
        if random.random() < 0.5:
            self.xp_list.append(XP(self.center_x + random.randint(3, 5), self.center_y + random.randint(3, 5)))

    def check_collisions(self):
        enemy_collisions = arcade.check_for_collision_with_list(self, self.enemy_array)

        if len(enemy_collisions) >= 1 or arcade.check_for_collision(self, self.player):
            self.center_x -= self.change_x
            self.center_y -= self.change_y
            self.change_x = 0
            self.change_y = 0
            self._state = self.animation_state.IDLE

    def set_animation_direction(self, direction):
        self.direction = direction

    def set_direction_to_player(self, delta_time: float):
        target_x = self.player.center_x
        target_y = self.player.center_y
        origin_x, origin_y = self.get_position()

        self.center_x = origin_x
        self.center_y = origin_y
        direction = Vec2(target_x - origin_x, target_y - origin_y).normalize() * self.speed * delta_time
        self.change_x = direction.x
        self.change_y = direction.y

    def draw(self, *, draw_filter=None, pixelated=None, blend_function=None):
        super().draw(filter=draw_filter, pixelated=pixelated, blend_function=blend_function)

    def get_state(self):
        return self._state

    def update(self):
        self.update_direction()

    def update_enemy_speed(self, delta_time: float):
        pass

    def shoot(self):
        pass


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
    SPEED = 200

    TEXTURES = SKELETON_TEXTURES_BASE

    def __init__(self, player: Player, enemy_array: SpriteList, enemy_projectile_list: SpriteList,
                 player_projectile_list: SpriteList, xp_list):
        super().__init__(player, enemy_array, enemy_projectile_list, player_projectile_list, xp_list,
                         Skeleton.SPEED, 5,
                         SkeletonAnimationState.IDLE, Direction.RIGHT,
                         SkeletonAnimationState,
                         Skeleton.SPRITE_SCALE)

    def load_textures(self) -> dict:
        """loads the right textures of the sprite
        """
        if Skeleton.TEXTURES == SKELETON_TEXTURES_BASE:
            textures = load_textures(":data:enemies/skeleton", SkeletonAnimationState)
        else:
            textures = Skeleton.TEXTURES

        return textures

    def on_update(self, delta_time: float = 1 / 60):
        """Updates player position and checks for collision
        Run this function every update of the window

        """
        # distance_of_attack = 50
        # top_y_distance_of_attack = 15
        # bottom_y_distance_of_attack = -130
        #
        # self.update_enemy_speed(delta_time)
        #
        # self.center_x += self.change_x
        # self.center_y += self.change_y
        #
        # self.check_death(Skeleton)
        #
        # if self._state != self.animation_state.DEATH:
        #     self.check_collisions()
        #
        #     if self.change_x != 0 or self.change_y != 0:
        #         self._state = self.animation_state.WALK
        #     else:
        #         if (abs(self.player.center_x - self.left) <= distance_of_attack or
        #             abs(self.right - self.player.center_x) <= distance_of_attack) and \
        #                 bottom_y_distance_of_attack <= self.center_y - \
        #                 self.player.center_y <= top_y_distance_of_attack and \
        #                 (self._state == self.animation_state.IDLE or self._state == self.animation_state.ATTACK):
        #             self._state = self.animation_state.ATTACK
        #             if self.current_texture_index + 1 >= self._state.value[1] and \
        #                     self.frame_counter + 1 > self.frames_per_texture:
        #                 self.player.reduce_health(2)

        if self._state.value[0] != self.animation_state.value[0]:
            self.update_state(self.animation_state)
        self.update_direction()

        # check_map_bounds(self)

    def update_enemy_speed(self, delta_time: float):
        """Updates slimes change_x and change_y

        Changes these values in accordance to the location of the player
        """

        self.set_direction_to_player(delta_time)


class Archer(AEnemy):
    """Archer Class

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
    SPEED = 300

    TEXTURES = ARCHER_TEXTURES_BASE

    def __init__(self, player: Player, enemy_array: SpriteList, enemy_projectile_list: SpriteList,
                 player_projectile_list: SpriteList, xp_list: SpriteList):
        super().__init__(player, enemy_array, enemy_projectile_list, player_projectile_list, xp_list,
                         Archer.SPEED, 5,
                         ArcherAnimationState.IDLE, Direction.RIGHT,
                         ArcherAnimationState,
                         Archer.SPRITE_SCALE)

    def load_textures(self) -> dict:
        """loads the right textures of the sprite
        """
        if Archer.TEXTURES == ARCHER_TEXTURES_BASE:
            textures = load_textures(":data:enemies/archer", ArcherAnimationState)
        else:
            textures = Archer.TEXTURES

        return textures

    def shoot(self):
        arrow_path = ":data:enemies/archer/arrow/0.png"
        if self.direction == Direction.LEFT:
            source_x = self.center_x + 30
        else:
            source_x = self.center_x - 30
        self.enemy_projectile_list.append(
            Projectile(source_x, self.center_y, self.player.center_x, self.player.center_y, arrow_path))

    def on_update(self, delta_time: float = 1 / 60):
        """Updates player position and checks for collision
        Run this function every update of the window

        """
        max_distance_of_attack = 700

        self.update_enemy_speed(delta_time)

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.check_death(Archer)

        if self._state != self.animation_state.DEATH:
            self.check_collisions()

            distance_to_player = sqrt(
                abs(self.center_x - self.player.center_x) ** 2 + abs(
                    self.center_y - self.player.center_y) ** 2)

            if self.change_x != 0 or self.change_y != 0:
                self._state = self.animation_state.WALK
            elif distance_to_player <= max_distance_of_attack and (self._state == self.animation_state.IDLE or
                                                                   self._state == self.animation_state.ATTACK):
                self._state = self.animation_state.ATTACK
                if self.current_texture_index + 1 >= self._state.value[1] and \
                        self.frame_counter + 1 > self.frames_per_texture:
                    self.shoot()
            else:
                self._state = self.animation_state.IDLE

            self.set_animation_direction(self.direction)

        check_map_bounds(self)

    def update_enemy_speed(self, delta_time: float):
        """Updates slimes change_x and change_y

        Changes these values in accordance to the location of the player
        """
        min_distance_to_player = 300
        mam_distance_to_player = 500
        target_x = self.player.center_x
        target_y = self.player.center_y

        self.set_direction_to_player(delta_time)

        distance_to_player = sqrt(abs(target_x - self.center_x) ** 2 + abs(target_y - self.center_y) ** 2)
        if distance_to_player < min_distance_to_player:
            self.change_x = -self.change_x
            self.change_y = -self.change_y
        elif distance_to_player < mam_distance_to_player:
            self.change_x = 0
            self.change_y = 0


class Slime(AEnemy):
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

    FRAMES_PER_TEXTURE = 10
    SPEED = 200

    TEXTURES = SLIME_TEXTURES_BASE

    def __init__(self, player: Player, enemy_array: SpriteList, enemy_projectile_list: SpriteList,
                 player_projectile_list: SpriteList, xp_list: SpriteList, sprite_scale=5, parent=True,
                 starting_x=random.randint(0, constants.MAP_WIDTH), starting_y=random.randint(0, constants.MAP_HEIGHT),
                 do_start_collision_checking=True):
        self.sprite_scale = sprite_scale
        super().__init__(player, enemy_array, enemy_projectile_list, player_projectile_list, xp_list, Slime.SPEED, 5,
                         SlimeAnimationState.IDLE, Direction.LEFT,
                         SlimeAnimationState,
                         self.sprite_scale,
                         starting_x,
                         starting_y,
                         do_start_collision_checking=do_start_collision_checking)
        self.parent = parent
        self.xp_list = xp_list

    def load_textures(self) -> dict:
        """loads the right textures of the sprite
        """
        if Slime.TEXTURES == SKELETON_TEXTURES_BASE:
            textures = load_textures(":data:enemies/slime", SlimeAnimationState)
        else:
            textures = Slime.TEXTURES

        return textures

    def on_update(self, delta_time: float = 1 / 60):
        """Updates player position and checks for collision
        Run this function every update of the window

        """
        distance_of_attack = 50
        top_y_distance_of_attack = 15
        bottom_y_distance_of_attack = -130

        self.update_enemy_speed(delta_time)
        self.set_animation_direction(self.direction)

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.check_death(Slime)

        if self._state != self.animation_state.DEATH:
            self.check_collisions()

            if self.change_x != 0 or self.change_y != 0:
                self._state = self.animation_state.WALK
            else:
                if (abs(self.player.center_x - self.left) <= distance_of_attack or
                    abs(self.right - self.player.center_x) <= distance_of_attack) and \
                        bottom_y_distance_of_attack <= self.center_y - \
                        self.player.center_y <= top_y_distance_of_attack and \
                        (self._state == self.animation_state.IDLE):
                    if self.current_texture_index + 1 >= self._state.value[1] and \
                            self.frame_counter + 1 > self.frames_per_texture:
                        self.player.reduce_health(2)

            self.check_collisions()

        check_map_bounds(self)

    def update_enemy_speed(self, delta_time: float):
        """Updates slimes change_x and change_y

        Changes these values in accordance to the location of the player
        """

        self.set_direction_to_player(delta_time)

    def check_death(self, enemy_to_spawn):
        if self._state != self.animation_state.DEATH:
            for projectile in self.player_projectile_list:
                if arcade.check_for_collision(self, projectile):
                    self._state = self.animation_state.DEATH
                    projectile.remove_from_sprite_lists()

        if self._state == self.animation_state.DEATH:
            self.center_x -= self.change_x
            self.center_y -= self.change_y
            if self.current_texture_index + 1 >= self._state.value[1] and \
                    self.frame_counter + 1 > self.frames_per_texture:
                if self.parent:
                    places = [[-40, -40], [-40, 40], [40, 40], [40, -40]]
                    for place in places:
                        self.enemy_array.append(Slime(self.player, self.enemy_array,
                                                      self.enemy_projectile_list, self.player_projectile_list,
                                                      self.xp_list, 2, False, starting_x=int(self.center_x + place[0]),
                                                      starting_y=int(self.center_y + place[1]),
                                                      do_start_collision_checking=False))
                        self.enemy_array.append(enemy_to_spawn(self.player, self.enemy_array,
                                                               self.enemy_projectile_list, self.player_projectile_list,
                                                               self.xp_list))

                self.remove_from_sprite_lists()

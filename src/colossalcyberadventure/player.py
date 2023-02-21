from enum import Enum

from arcade import SpriteList
from pyglet.math import Vec2

import arcade.key as k

from entity import IEntity
from constants import *
from projectile import Projectile

from src.colossalcyberadventure.healthbar import HealthBar
from src.colossalcyberadventure.weapons import Weapon
from src.colossalcyberadventure.inventory import Inventory
import arcade


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
            tex_left, tex_right = arcade.load_texture_pair(f"resources/player/{state.value[0]}/{i}.png")
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

    SPEED = 7
    FRAMES_PER_TEXTURE = 5

    def __init__(self, enemy_projectile_list: SpriteList, player_projectile_list: SpriteList,
                 keyboard_state: dict[int, bool]):
        super().__init__(scale=Player.SPRITE_SCALE)
        if textures == TEXTURES_BASE:
            load_textures()
        self.skill_cooldown = 0
        self.keyboard_state = keyboard_state
        self.player_projectile_list = player_projectile_list
        self.enemy_projectile_list = enemy_projectile_list
        self.center_x = MAP_WIDTH // 2
        self.center_y = MAP_HEIGHT // 2
        self.delta_change_x = 0
        self.delta_change_y = 0
        self._state = PlayerAnimationState.IDLE
        self.direction = Direction.RIGHT
        self.texture = textures[PlayerAnimationState.IDLE][self.direction][0]
        self.frame_counter = 0
        self.current_texture_index = 0
        self.health_bar = HealthBar(self, 70, 5, 1, arcade.color.BLACK, arcade.color.RED)
        self.should_reset_sprite_counter = False
        self.inventory = Inventory(owner=self)

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

        self.frame_counter += 1
        if self.frame_counter > Player.FRAMES_PER_TEXTURE:
            self.frame_counter = 0

    def update(self):
        """Updates player position and checks for collision
        Run this function every update of the window

        """
        BULLET_PATH = "resources/bullet/0.png"
        SKILL_COOLDOWN = 100

        self.center_x += self.change_x
        self.center_y += self.change_y



        for projectile in self.enemy_projectile_list:
            if arcade.check_for_collision(self, projectile):
                if self.health_bar.health_points > 0:
                    self.health_bar.health_points -= 2
                # ToDo add death
                projectile.remove_from_sprite_lists()

        old_direction = self.direction
        if self.change_x < 0:
            self.direction = Direction.LEFT
        elif self.change_x > 0:
            self.direction = Direction.RIGHT

        if old_direction != self.direction:
            self.should_reset_sprite_counter = True

        if self.left < 0:
            self.left = 0
        if self.right > MAP_WIDTH - 1:
            self.right = MAP_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        if self.top > MAP_HEIGHT - 1:
            self.top = MAP_HEIGHT - 1

        self.health_bar.update()

        if self.skill_cooldown == 0:
            directions = [[self.center_x, self.center_y + 1], [self.center_x + 1, self.center_y + 1],
                          [self.center_x + 1, self.center_y], [self.center_x + 1, self.center_y - 1],
                          [self.center_x, self.center_y - 1], [self.center_x - 1, self.center_y - 1],
                          [self.center_x - 1, self.center_y], [self.center_x - 1, self.center_y + 1]
                          ]
            if self.keyboard_state[k.C]:
                self.skill_cooldown += 1
                for i in range(8):
                    self.player_projectile_list.append(
                        Projectile(self.center_x, self.center_y, directions[i][0], directions[i][1], BULLET_PATH, 2))
        else:
            self.skill_cooldown += 1
            if self.skill_cooldown == SKILL_COOLDOWN:
                self.skill_cooldown = 0



    def get_position(self) -> tuple[float, float]:
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

    def update_player_speed(self, keyboard_state: dict[int, bool]):
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

        movement_vec = movement_vec.normalize() * Vec2(Player.SPEED, Player.SPEED)
        self.change_x = movement_vec.x
        self.change_y = movement_vec.y

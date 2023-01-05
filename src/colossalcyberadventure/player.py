from enum import Enum

from entity import IEntity
import arcade


class TextureState(Enum):
    IDLE = ("idle", 7)
    WALK = ("walk", 7)


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"


textures = {TextureState.IDLE: {"left": [], "right": []}, TextureState.WALK: {"left": [], "right": []}}


class Player(arcade.Sprite, IEntity):

    SPEED = 7

    def __init__(self):
        super().__init__()
        # ---------Load Textures---------
        for state in TextureState:
            for i in range(state.value[1] + 1):
                left, right = arcade.texture.load_texture_pair(f"res/{state.value[0]}/{i}.png")
                textures[state]["left"].append(left)
                textures[state]["right"].append(right)
        # -------------------------------

    def update(self):
        """ Updates player position
        Run this function every update of the window

        """
        self.center_x += self.change_x
        self.center_y += self.change_y

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
        """Updates player change_x and change_y values
        Changes these values in accordance to the currently pressed keys

        """
        self.change_x = 0
        self.change_y = 0

        if keyboard_state[arcade.key.W] and not keyboard_state[arcade.key.S]:
            self.change_y = Player.SPEED
        elif keyboard_state[arcade.key.S] and not keyboard_state[arcade.key.W]:
            self.change_y = -Player.SPEED
        if keyboard_state[arcade.key.A] and not keyboard_state[arcade.key.D]:
            self.change_x = -Player.SPEED
        elif keyboard_state[arcade.key.D] and not keyboard_state[arcade.key.A]:
            self.change_x = Player.SPEED

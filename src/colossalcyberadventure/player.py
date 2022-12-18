from entity import IEntity
import arcade


class Player(arcade.Sprite, IEntity):

    SPEED = 7

    def __init__(self, resource_name):
        super().__init__(resource_name)

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

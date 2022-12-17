from entity import IEntity
import arcade


class Player(arcade.Sprite, IEntity):
    def __init__(self, resource_name, speed):
        super().__init__(resource_name)
        self.speed = speed

    def update(self):
        """ Updates player position
        Run this function every update of the window

        """
        self.center_x += self.change_x
        self.center_y += self.change_y

    def get_position(self) -> tuple:
        """Returns the player position relative to the map

        Returns
        -------
        int
            x value of player center
        int
            y value of player center
        """

        return self.center_x, self.center_y

    def update_player_speed(self, keyboard_state: dict[int, bool]):
        """Updates player change_x and change_y values
        Changes these values in accordance to the currently pressed keys

        """
        self.change_x = 0
        self.change_y = 0

        if keyboard_state[arcade.key.W] and not keyboard_state[arcade.key.S]:
            self.change_y = self.speed
        elif keyboard_state[arcade.key.S] and not keyboard_state[arcade.key.W]:
            self.change_y = -self.speed
        if keyboard_state[arcade.key.A] and not keyboard_state[arcade.key.D]:
            self.change_x = -self.speed
        elif keyboard_state[arcade.key.D] and not keyboard_state[arcade.key.A]:
            self.change_x = self.speed


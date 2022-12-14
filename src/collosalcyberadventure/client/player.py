from entity import IEntity
import arcade


class Player(arcade.Sprite, IEntity):
    def __init__(self, resource_name, speed):
        super().__init__(resource_name)
        self.speed = speed

    def update(self):
        """ Updates player position

        """
        self.center_x += self.change_x
        self.center_y += self.change_y

    def get_position(self) -> tuple:
        """returns the player relative position to the map

        :return:
        tuple(int, int) : tuple that contains player x, y position
        """

        return tuple(self.center_x, self.center_y)

    def update_player_speed(self, keyboard_state: dict[int, bool]):
        """ Updates player speed
         what direction he should move to according to what key was pressed

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


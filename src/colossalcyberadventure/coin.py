from colossalcyberadventure.entity import IEntity
import arcade


class Coin(arcade.Sprite, IEntity):
    def __init__(self, resource_name, pos_x, pos_y):
        super().__init__(resource_name)
        self.center_x = pos_x
        self.center_y = pos_y

    def get_position(self) -> tuple[float, float]:
        """returns the coin relative position to the map

        :return:
        tuple(int, int) : tuple that contains player x, y position
        """

        return self.center_x, self.center_y


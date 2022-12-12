from entity import IEntity
import arcade


class Player(arcade.Sprite, IEntity):
    def __init__(self, resource_name, speed):
        super().__init__(resource_name)
        # self.a_pressed = False
        # self.d_pressed = False
        # self.w_pressed = False
        # self.s_pressed = False
        self.speed = speed

    def update(self):
        """ Updates player position

        Returns
        -------
        None
        """
        self.center_x += self.change_x
        self.center_y += self.change_y

    def getX(self):
        """ Returns player's X coordinate

        Returns
        -------
        int: Player's X coordinate
        """
        return self.center_x

    def getY(self):
        """ Returns player's Y coordinate

        Returns
        -------
        int: Player's Y coordinate
        """
        return self.center_y

    def update_player_speed(self, keyboard_state: dict[str, bool]):
        """ Updates player speed - what direction he should move to according to what key was pressed

        Returns
        -------
        None
        """
        self.change_x = 0
        self.change_y = 0

        if keyboard_state["w"] and not keyboard_state["s"]:
            self.change_y = self.speed
        elif keyboard_state["s"] and not keyboard_state["w"]:
            self.change_y = -self.speed
        if keyboard_state["a"] and not keyboard_state["d"]:
            self.change_x = -self.speed
        elif keyboard_state["d"] and not keyboard_state["a"]:
            self.change_x = self.speed



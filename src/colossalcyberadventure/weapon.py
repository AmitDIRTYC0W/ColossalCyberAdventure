from math import atan2, degrees

import arcade

from colossalcyberadventure.player import Player, Direction, PlayerAnimationState


class AWeapon(arcade.Sprite):
    Sprite_Path = "resources/bullet/0.png"

    def __init__(self, player: Player):
        super().__init__("resources/bullet/0.png")
        self.player = player
        self.player_direction = self.player.get_direction()
        self.player_state = self.player.get_state()
        self.player_x, self.player_y = self.player.get_position()

    def update(self):
        self.player_direction = self.player.get_direction()
        self.player_state = self.player.get_state()
        self.player_x, self.player_y = self.player.get_position()
        self.center_x = self.player_x
        self.center_y = self.player_y - 40
        if self.player_state is PlayerAnimationState.WALK:
            self.center_y = self.player_y - 10
        else:
            if self.player_direction is Direction.LEFT:
                self.center_x -= 80
            elif self.player_direction is Direction.RIGHT:
                self.center_x += 80


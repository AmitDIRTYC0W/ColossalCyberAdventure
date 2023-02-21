import arcade

from colossalcyberadventure.player import Player, Direction, PlayerAnimationState


class AWeapon(arcade.Sprite):
    Sprite_Path = "resources/player/skull/0.png"

    def __init__(self, player: Player):
        super().__init__("resources/player/skull/0.png", scale=1.5)
        self.player = player
        self.player_direction = self.player.get_direction()
        self.player_x, self.player_y = self.player.get_position()

    def update(self):
        self.player_direction = self.player.get_direction()
        self.player_x, self.player_y = self.player.get_position()
        self.center_x = self.player_x
        self.center_y = self.player_y - 37
        if PlayerAnimationState.WALK.value[0] == self.player.get_state().value[0]:
            self.center_y = self.center_y - 13
        else:
            if self.player.get_direction().value[0] is Direction.LEFT.value[0]:
                self.center_x += 27
            else:
                self.center_x -= 27

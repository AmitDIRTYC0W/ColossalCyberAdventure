import arcade

from .player import Player, Direction, PlayerAnimationState


class AWeapon(arcade.Sprite):

    def __init__(self, player: Player):
        SPRITE_SCALE = 1.5
        super().__init__(":data:player/skull/0.png", scale=SPRITE_SCALE)
        self.player = player
        self.player_direction = self.player.get_direction()
        self.player_x, self.player_y = self.player.get_position()

    def update(self):
        WEAPON_X_OFFSET = 27
        WEAPON_INITIAL_OFFSET = 37
        WEAPON_WALKING_OFFSET = 13
        self.player_direction = self.player.get_direction()
        self.player_x, self.player_y = self.player.get_position()
        self.center_x = self.player_x
        self.center_y = self.player_y - WEAPON_INITIAL_OFFSET
        if PlayerAnimationState.WALK.value[0] == self.player.get_state().value[0]:
            self.center_y = self.center_y - WEAPON_WALKING_OFFSET
        else:
            if self.player.get_direction().value[0] is Direction.LEFT.value[0]:
                self.center_x += WEAPON_X_OFFSET
            else:
                self.center_x -= WEAPON_X_OFFSET

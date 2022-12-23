import random
from typing import Final
import arcade

from arcade import key as k

from src.colossalcyberadventure.coin import Coin
from src.colossalcyberadventure.player import Player


class ColossalCyberAdventure(arcade.Window):
    """ Main window class

    Attributes
    ----------
    width : int
        pixels, greater than 0
    height:
        pixels, greater than 0
    title : str
    """

    BACKGROUND_COLOR = arcade.color.AMAZON

    def __init__(self,
                 width: int,
                 height: int,
                 title: str, ):
        super().__init__(width, height, title)
        self.width: Final[int] = width
        self.height: Final[int] = height
        self.title: Final[str] = title

        arcade.set_background_color(ColossalCyberAdventure.BACKGROUND_COLOR)

    def setup(self):
        """Set up window

        Sets up window. Call this again to restart game.
        """
        self.show_view(GameView())


class GameView(arcade.View):
    """View of the actual game
    """
    BACKGROUND_COLOR = arcade.color.JET

    COIN_NUM = 10

    def __init__(self):
        super().__init__()

        self.player = Player("resources/kanye_sprite.png")
        self.coins: list[Coin] = []
        for i in range(GameView.COIN_NUM):
            self.coins.append(Coin("resources/coin_sprite.png", random.randint(0, self.window.width),
                                   random.randint(0, self.window.height)))
        self.pressed_keys = {k.W: False, k.A: False, k.S: False, k.D: False}

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

    def on_draw(self):
        self.clear()

        self.player.draw()

        for coin in self.coins:
            coin.draw()

    def on_update(self, delta_time: float):
        self.player.update_player_speed(self.pressed_keys)
        self.player.update()

        self.game_camera.move_to()

        for i, coin in enumerate(self.coins):
            if arcade.check_for_collision(self.player, coin):
                self.coins.pop(i)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.pressed_keys.keys():
            self.pressed_keys[symbol] = True

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.pressed_keys.keys():
            self.pressed_keys[symbol] = False

import random
import arcade

from collosalcyberadventure.client.keyboard import IKeyboardHandler
from collosalcyberadventure.client.player import Player
from collosalcyberadventure.client.window import IWindow
from collosalcyberadventure.client.coin import Coin

class KeyboardHandler(IKeyboardHandler):

    def __init__(self):
        self.pressed_keys = {arcade.key.W: False, arcade.key.A: False, arcade.key.S: False, arcade.key.D: False}

    def get_pressed_keys(self) -> dict[int, bool]:
        return self.pressed_keys

    def set_key(self, key: int, value: bool):
        if key in self.pressed_keys.keys():
            self.pressed_keys[key] = value


class GameWindow(IWindow):
    def __init__(self):
        super().__init__()
        self.player_sprite: Player | None = None
        self.keyboard_handler = KeyboardHandler()
        self.coin_list: Coin | None = None

    def setup(self):
        self.coin_list = arcade.SpriteList()
        for i in range(10):
            coin = Coin("resources/coin_sprite.png", random.randrange(800), random.randrange(800))
            self.coin_list.append(coin)
            print(coin.get_position())


        self.player_sprite = Player("resources/kanye_sprite.png", 7)



    def on_draw(self):
        self.clear()

        self.coin_list.draw()
        self.player_sprite.draw()

        self.player_sprite.update_player_speed(self.keyboard_handler.get_pressed_keys())
        self.player_sprite.update()
        print(self.player_sprite.get_position())

    def get_keyboard_handler(self) -> IKeyboardHandler:
        return self.keyboard_handler

    def on_key_press(self, symbol: int, modifiers: int):
        self.keyboard_handler.set_key(symbol, True)

    def on_key_release(self, symbol: int, modifiers: int):
        self.keyboard_handler.set_key(symbol, False)

    def update(self, delta_time: float):
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()


def main():
    window = GameWindow()
    window.setup()
    window.run()


if __name__ == '__main__':
    main()

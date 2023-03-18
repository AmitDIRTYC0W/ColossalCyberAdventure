import arcade

from colossalcyberadventure import constants
from .item import Coin
from .item import HealthShroom
from .constants import *


class ItemSlot(arcade.Sprite):
    ITEM_SLOT_PATH = ":data:inventory/item_slot.png"

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(ItemSlot.ITEM_SLOT_PATH)
        self.center_x = 0  # placeholder
        self.center_y = 0  # placeholder
        self.item = None
        self.touched_flag = False

    def on_press_item(self, mouse_x, mouse_y):
        bottom_left_x = self.center_x - self.width / 2
        bottom_left_y = self.center_y - self.height / 2
        top_right_x = self.center_x + self.width / 2
        top_right_y = self.center_y + self.height / 2
        if bottom_left_x <= mouse_x <= top_right_x and bottom_left_y <= mouse_y <= top_right_y:
            self.touched_flag = not self.touched_flag


class PlayerHead(ItemSlot):
    PLAYER_HEAD_PATH = ":data:inventory/player_head.png"

    def __init__(self):
        super().__init__()
        # self.alpha = 255
        self.texture = arcade.load_texture(PlayerHead.PLAYER_HEAD_PATH)


class Inventory:

    def __init__(self, coin_counter: int, health_shroom_counter: int, player, owner: "Player"):
        self.owner = owner
        self.player = player
        self.owner_x = owner.get_position()[0]
        self.owner_y = owner.get_position()[1]
        self.coin_counter = coin_counter
        self.health_shroom_counter = health_shroom_counter
        self.coins_indicator = Coin(self.owner_x, self.owner_y)
        self.shroom_indicator = HealthShroom(self.owner_x, self.owner_y)
        self.player_indicator = PlayerHead()

    def update(self, camera_x, camera_y):
        self.coin_counter = self.player.coin_counter
        self.health_shroom_counter = self.player.health_shroom_counter
        self.coins_indicator.center_x = camera_x + constants.WIDTH / 2
        self.coins_indicator.center_y = camera_y + constants.SCREEN_HEIGHT / 2
        self.shroom_indicator.center_x = camera_x + 1.5 * constants.WIDTH + constants.MARGIN
        self.shroom_indicator.center_y = camera_y + constants.SCREEN_HEIGHT / 2
        self.player_indicator.center_x = camera_x + constants.WIDTH / 2 + MARGIN * 3
        self.player_indicator.center_y = camera_y + constants.SCREEN_HEIGHT / 2 - (constants.HEIGHT + MARGIN)

    def draw(self):
        if self.coin_counter != 0:
            self.coins_indicator.draw()
            arcade.draw_text(f"X{self.coin_counter}",
                             start_x=self.coins_indicator.center_x + 100 / 2,
                             start_y=self.coins_indicator.center_y - 110 / 2,
                             bold=True,
                             font_size=15)
        if self.health_shroom_counter != 0:
            self.shroom_indicator.draw()
            arcade.draw_text(f"X{self.health_shroom_counter}",
                             start_x=self.shroom_indicator.center_x + 100 / 2,
                             start_y=self.shroom_indicator.center_y - 110 / 2,
                             bold=True,
                             font_size=15)
        self.player_indicator.draw()
        arcade.draw_text(f"YOU:",
                         start_x=self.player_indicator.center_x - 130 / 2,
                         start_y=self.player_indicator.center_y - 135 / 2,
                         bold=True,
                         font_size=15)

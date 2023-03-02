import arcade

from src.colossalcyberadventure.entity import IEntity
from src.colossalcyberadventure.constants import *
import constants


class ItemSlot(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("resources/inventory/item_slot.png")
        self.center_x = -99  # placeholder
        self.center_y = -99  # placeholder
        self.item = None
        self.alpha = 99
        self.touched_flag = False

    def is_touched(self, mouse_x, mouse_y):
        bottom_left_x = self.center_x - self.width / 2
        bottom_left_y = self.center_y - self.height / 2
        top_right_x = self.center_x + self.width / 2
        top_right_y = self.center_y + self.height / 2
        if bottom_left_x <= mouse_x <= top_right_x and bottom_left_y <= mouse_y <= top_right_y:
            self.touched_flag = not self.touched_flag


class CoinIndicator(ItemSlot):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("resources/items/coin.png")
        self.counter = 0
        self.alpha = 255


class ShroomIndicator(ItemSlot):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("resources/items/HPSHROOM.png")
        self.counter = 0
        self.alpha = 255
        self.scale = 0.9


class PlayerHead(ItemSlot):
    def __init__(self):
        super().__init__()
        self.alpha = 255
        self.texture = arcade.load_texture("resources/inventory/player_head.png")


class Inventory:

    def __init__(self, owner: IEntity):
        # self.width = 405
        # self.height = 1080
        self.owner = owner
        self.owner_x = owner.get_position()[0]
        self.owner_y = owner.get_position()[1]
        # self.center_x = -1  # placeholder
        # self.center_y = -1  # placeholder
        # self.grid_sprite_list = arcade.SpriteList()
        self.coins_indicator = CoinIndicator()
        self.shroom_indicator = ShroomIndicator()
        self.player_indicator = PlayerHead()

        # for row in range(ROW_COUNT):
        #     for column in range(COLUMN_COUNT):
        #         self.grid_sprite_list.append(ItemSlot())

        # def update_color(self):
        #     for item_slot in self.grid_sprite_list:
        #         if item_slot.touched_flag:
        #             item_slot.alpha = 255
        #         if not item_slot.touched_flag:
        #             item_slot.alpha = 99

    def update(self, camera_x, camera_y):
        # self.owner_x = self.owner.get_position()[0]
        # self.owner_y = self.owner.get_position()[1]
        # self.center_x = camera_x + constants.SCREEN_WIDTH - (405 / 2)
        # self.center_y = camera_y + constants.SCREEN_WIDTH / 2
        # i = 0
        # for row in range(ROW_COUNT):
        #     for column in range(COLUMN_COUNT):
        #         x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        #         y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + (
        #                     (constants.SCREEN_HEIGHT / 2) - (2 * HEIGHT + MARGIN))
        #         self.grid_sprite_list[i].center_x = x + camera_x + constants.SCREEN_WIDTH - ((WIDTH + MARGIN) * 3)
        #         self.grid_sprite_list[i].center_y = y + camera_y
        #         i += 1
        self.coins_indicator.counter = constants.COIN_COUNTER
        self.coins_indicator.center_x = camera_x + constants.WIDTH/2
        self.coins_indicator.center_y = camera_y + constants.SCREEN_HEIGHT/2
        self.shroom_indicator.counter = constants.SHROOM_COUNTER
        self.shroom_indicator.center_x = camera_x + 1.5*constants.WIDTH + constants.MARGIN
        self.shroom_indicator.center_y = camera_y + constants.SCREEN_HEIGHT/2
        self.player_indicator.center_x = camera_x + constants.WIDTH/2 + MARGIN*3
        self.player_indicator.center_y = camera_y + constants.SCREEN_HEIGHT/2 - (constants.HEIGHT + MARGIN)
        # self.update_color()

    def draw(self):
        # arcade.draw_rectangle_filled(color=(255, 255, 255), center_x=self.center_x,
        #                             center_y=self.center_y, width=self.width, height=self.height, alpha)
        # self.grid_sprite_list.draw()
        self.coins_indicator.draw()
        arcade.draw_text(f"X{self.coins_indicator.counter}",
                         start_x=self.coins_indicator.center_x + 100/2,
                         start_y=self.coins_indicator.center_y - 110/2,
                         bold=True,
                         font_size=15)
        self.shroom_indicator.draw()
        arcade.draw_text(f"X{self.shroom_indicator.counter}",
                         start_x=self.shroom_indicator.center_x + 100/2,
                         start_y=self.shroom_indicator.center_y - 110/2,
                         bold=True,
                         font_size=15)
        self.player_indicator.draw()
        arcade.draw_text(f"YOU:",
                         start_x=self.player_indicator.center_x - 130/2,
                         start_y=self.player_indicator.center_y - 135/2,
                         bold=True,
                         font_size=15)

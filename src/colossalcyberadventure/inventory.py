import arcade

from src.colossalcyberadventure.entity import IEntity

ROW_COUNT = 8
COLUMN_COUNT = 3


WIDTH = 130
HEIGHT = 130


MARGIN = 5



class ItemSlot(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("resources/inventory/item_slot.png")
        self.center_x = -99  # placeholder
        self.center_y = -99  # placeholder
        self.item = None

    def set_texture(self):
        pass


class Inventory:

    def __init__(self, owner: IEntity):
        self.width = 405
        self.height = 1080
        self.owner = owner
        self.owner_x = owner.get_position()[0]
        self.owner_y = owner.get_position()[1]
        self.center_x = -1  # placeholder
        self.center_y = -1  # placeholder
        self.grid = []

        for row in range(ROW_COUNT):
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(ItemSlot())



    def update(self, camera_x, camera_y):
        self.owner_x = self.owner.get_position()[0]
        self.owner_y = self.owner.get_position()[1]
        self.center_x = camera_x + 1920 - (405 / 2)
        self.center_y = camera_y + 1080 / 2

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                self.grid[row][column].center_x = x + camera_x + 1920-((130+MARGIN)*3)
                self.grid[row][column].center_y = y + camera_y

    def draw(self):
        arcade.draw_rectangle_filled(color=(255, 255, 255), center_x=self.center_x,
                                     center_y=self.center_y, width=self.width, height=self.height)
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                self.grid[row][column].draw()

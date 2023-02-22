import arcade

from src.colossalcyberadventure.entity import IEntity

ROW_COUNT = 8
COLUMN_COUNT = 3

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 130
HEIGHT = 130

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5


class Inventory:
    def __init__(self, owner: IEntity):
        self.width = 405
        self.height = 1080
        self.owner = owner
        self.owner_x = owner.get_position()[0]
        self.owner_y = owner.get_position()[1]
        self.center_x = -1  # placeholder
        self.center_y = -1  # placeholder
        self.grid_sprite_list = arcade.SpriteList()
        self.grid_sprites = []

    def update(self, camera_x, camera_y):
        self.grid_sprite_list.clear()
        self.owner_x = self.owner.get_position()[0]
        self.owner_y = self.owner.get_position()[1]
        self.center_x = camera_x + 1920-(405/2)
        self.center_y = camera_y + 1080/2
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.DARK_GRAY)
                sprite.center_x = x + camera_x + 1920-((130+MARGIN)*3)
                sprite.center_y = y + camera_y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

    def draw(self):
        arcade.draw_rectangle_filled(color=(255, 255, 255), center_x=self.center_x,
                                     center_y=self.center_y, width=self.width, height=self.height)

        self.grid_sprite_list.draw()


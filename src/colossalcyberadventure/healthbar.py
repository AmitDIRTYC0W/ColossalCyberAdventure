import arcade
from arcade import Text


class HealthBar:
    VERTICAL_OFFSET = 45
    STARTING_HP = 80
    RECT_WIDTH = 160
    RECT_HEIGHT = 25
    BORDER_THICKNESS = 2
    INNER_RECT_COLOR = (36, 93, 45)
    FULL_HEALTH = 100
    LEVEL_TEXT_OFFSET = 15

    def __init__(self, owner, width: float, height: float, outer_border_width,
                 outer_color: tuple[int, int, int], inner_color: tuple[int, int, int]):
        self.health_points = HealthBar.STARTING_HP

        self.owner = owner
        self.owner_x = owner.get_position()[0]
        self.owner_y = owner.get_position()[1]
        self.center_x = -1  # placeholder
        self.center_y = -1  # placeholder
        self.calculate_center_x_y()
        self.width = width
        self.height = height
        self.border_width = outer_border_width
        self.outer_color = outer_color

        self.inner_color = inner_color

        self.inner_width = -1  # placeholder
        self.inner_center_x = -1  # placeholder
        self.calculate_inner_values()
        self.level = owner.level
        self.level_text = Text(f"Level: {self.level}", self.center_x - self.width // 2,
                               self.center_y + HealthBar.LEVEL_TEXT_OFFSET, arcade.color.JET)

    def draw(self):
        self.calculate_inner_values()
        arcade.draw_rectangle_filled(self.inner_center_x, self.center_y, self.inner_width, self.height,
                                     self.inner_color)
        arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height, self.outer_color,
                                      self.border_width)
        self.level_text.draw()

    def calculate_center_x_y(self):
        self.center_x = self.owner_x
        self.center_y = self.owner_y + HealthBar.VERTICAL_OFFSET

    def calculate_inner_values(self):
        self.inner_width = self.health_points / HealthBar.FULL_HEALTH * (self.width - 2 * self.border_width)
        self.inner_center_x = self.center_x - (self.width - self.inner_width) / 2 + self.border_width

    def update_text_x_y(self):
        self.level_text.x = self.center_x - self.width // 2
        self.level_text.y = self.center_y + HealthBar.LEVEL_TEXT_OFFSET

    def update(self):
        self.level = self.owner.level
        self.owner_x = self.owner.get_position()[0]
        self.owner_y = self.owner.get_position()[1]
        self.calculate_center_x_y()
        self.calculate_inner_values()
        self.update_text_x_y()

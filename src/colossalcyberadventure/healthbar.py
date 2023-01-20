import arcade
from constants import *


class HealthBar:
    def __init__(self, player_x: float, player_y: float):
        self.health_points: float = HEALTH_POINTS  # 100 is full HP
        self.outer_rect_stats: dict = {"CENTER_X": player_x,
                                       "CENTER_Y": player_y + VERTICAL_OFFSET,
                                       "WIDTH": OUTER_RECTANGLE_WIDTH,
                                       "HEIGHT": OUTER_RECTANGLE_HEIGHT,
                                       "BORDER_WIDTH": OUTER_RECTANGLE_THICKNESS,
                                       "COLOR": arcade.color.BLACK
                                       }
        self.inner_rect_stats: dict = {"CENTER_X": player_x,
                                       "CENTER_Y": player_y + VERTICAL_OFFSET,
                                       "WIDTH": None,
                                       "HEIGHT": INNER_RECTANGLE_HEIGHT,
                                       "COLOR": INNER_RECTANGLE_COLOR
                                       }

    def set_inner_rectangle_width(self):
        self.inner_rect_stats["WIDTH"] = self.health_points * SCALE_HP_TO_HB

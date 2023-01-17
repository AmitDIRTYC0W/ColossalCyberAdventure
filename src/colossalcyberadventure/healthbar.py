import arcade


class HealthBar:
    def __init__(self, player_x: float, player_y: float):
        self.health_points: float = 50  # 100 is full HP
        self.outer_rect_stats: dict = {"CENTER_X": player_x,
                                       "CENTER_Y": player_y+45,
                                       "WIDTH": 160,
                                       "HEIGHT": 25,
                                       "BORDER_WIDTH": 2,
                                       "COLOR": arcade.color.BLACK
                                       }
        self.inner_rect_stats: dict = {"CENTER_X": player_x,
                                       "CENTER_Y": player_y+45,
                                       "WIDTH": None,
                                       "HEIGHT": 25,
                                       "COLOR": (36, 93, 45)
                                       }

    def set_health_box(self):
        self.inner_rect_stats["WIDTH"] = self.health_points*1.6


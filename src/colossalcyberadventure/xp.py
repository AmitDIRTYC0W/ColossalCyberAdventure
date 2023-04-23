import arcade


class XP(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":data:xp/0.png", scale=1.5)
        self.center_x = x
        self.center_y = y

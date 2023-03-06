import arcade


class AItem(arcade.Sprite):
    SPRITE_SCALE = 0.4

    def __init__(self, x_position: float, y_position: float):
        super().__init__()
        self.texture = self.load_textures()
        self.scale = AItem.SPRITE_SCALE
        self.center_x = x_position
        self.center_y = y_position

    def load_textures(self):
        raise NotImplementedError("load_textures() not implemented")

    def get_kind(self):
        return "item"


class Coin(AItem):
    Sprite_Scale = 0.4
    COIN_PATH = "resources/items/coin.png"

    def __init__(self, x_position: float, y_position: float):
        super().__init__(x_position, y_position)

    def load_textures(self):
        """loads the right textures of the sprite
        """
        texture = arcade.load_texture(Coin.COIN_PATH)
        return texture

    def get_kind(self):
        return "coin"


class HealthShroom(AItem):
    Sprite_Scale = 0.4
    SHROOM_PATH = "resources/items/HPSHROOM.png"

    def __init__(self, x_position: float, y_position: float):
        super().__init__(x_position, y_position)

    def load_textures(self):
        """loads the right textures of the sprite
        """
        texture = arcade.load_texture(HealthShroom.SHROOM_PATH)
        return texture

    def get_kind(self):
        return "shroom"

import arcade
from arcade import Camera

from colossalcyberadventure.player import Player


class HUD:
    def __init__(self, owner: Player, camera: Camera, view: arcade.View, width=60, height=60):
        super().__init__()
        self.owner = owner
        self.camera = camera
        self.view = view
        self.width, self.height = width, height
        self.coin_tex = arcade.load_texture(":data:items/coin.png")
        self.mushroom_tex = arcade.load_texture(":data:items/HPSHROOM.png")
        self.shown = False

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        if self.shown:
            arcade.draw_texture_rectangle(self.width // 2 + self.camera.position.x,
                                          self.camera.position.y + self.view.window.height // 2, self.width,
                                          self.height, self.coin_tex)
            arcade.draw_text(f"{self.owner.coin_counter}", self.width // 2 + self.width // 1.5 + self.camera.position.x,
                             self.camera.position.y + self.view.window.height // 2 - 17, arcade.color.BLACK, 40)

            arcade.draw_texture_rectangle(self.width // 2 + self.camera.position.x,
                                          self.camera.position.y + self.view.window.height // 2 + self.height,
                                          self.width, self.height, self.mushroom_tex)
            arcade.draw_text(f"{self.owner.mushroom_amount}", self.width // 2 + self.width // 1.5 + self.camera.position.x,
                             self.camera.position.y + self.view.window.height // 2 + self.height - 17,
                             arcade.color.BLACK, 40)

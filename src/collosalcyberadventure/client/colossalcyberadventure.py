from typing import Final

import arcade


class ColossalCyberAdventure(arcade.Window):
    """ Main window class

    Attributes
    ----------
    width : int
        pixels, greater than 0
    height:
        pixels, greater than 0
    title : str
    """

    BACKGROUND_COLOR = arcade.color.AMAZON

    def __init__(self,
                 width: int,
                 height: int,
                 title: str,):
        super().__init__(width, height, title)
        self.width: Final = width
        self.height: Final = height
        self.title: Final = title

        arcade.set_background_color(ColossalCyberAdventure.BACKGROUND_COLOR)

    def setup(self):
        """Set up window

        Sets up window. Call this again to restart game.
        """
        pass

    def on_draw(self):
        """Re-render screen

        Called once every frame
        """
        self.clear()
        # code to draw screen

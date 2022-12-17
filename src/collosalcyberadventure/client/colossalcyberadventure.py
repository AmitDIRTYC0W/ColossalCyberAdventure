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
        self.width: Final[int] = width
        self.height: Final[int] = height
        self.title: Final[str] = title

        arcade.set_background_color(ColossalCyberAdventure.BACKGROUND_COLOR)

    def setup(self):
        """Set up window

        Sets up window. Call this again to restart game.
        """
        self.show_view(GameView())


class GameView(arcade.View):
    """View of the actual game
    """
    BACKGROUND_COLOR = arcade.color.JET

    def __init__(self):
        super().__init__()

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

    def on_draw(self):
        self.clear()

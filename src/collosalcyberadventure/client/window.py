from typing import Final

import arcade


class Window(arcade.Window):
    """ Main window class

    Attributes
    ----------
    width : int > 0
    height: int > 0
    title : str
    background_color : tuple[int, int, int] | tuple[int, int, int, int]
    """
    def __init__(self,
                 width: int,
                 height: int,
                 title: str,
                 background_color: tuple[int, int, int] | tuple[int, int, int, int]):
        super().__init__(width, height, title)
        self.width: Final = width
        self.height: Final = height
        self.title: Final = title
        self.background_color = background_color

        arcade.set_background_color(background_color)

    def setup(self):
        """Set up window

        Sets up window. Call this once to restart game.

        Returns
        -------
        None
        """
        pass

    def on_draw(self):
        """Re-render screen

        Returns
        -------
        None
        """
        self.clear()
        # code to draw screen

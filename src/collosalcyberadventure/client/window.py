import arcade

from typing import Final

import arcade


class IWindow(arcade.Window):
    """Interface for the window class"""

    def setup(self):
        """Sets up window

        Sets up the game window. Called at the start of the game.

        Returns
        -------
        None
        """
        raise NotImplementedError("setup() method not implemented")

    def on_draw(self):
        """Draws the current frame

        Returns
        -------
        None
        """
        raise NotImplementedError("draw() method not implemented")


class Window(IWindow):
    """ Main window class

    Attributes
    ----------
    width : int > 0
    height: int > 0
    title : str
    background_color : tuple[int, int, int] | tuple[int, int, int, int]
    keyboard_handler : IKeyboardHandler
        saves the state of the keyboard and handles keyboard logic
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

        Sets up window. Call this again to restart game.

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

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W or symbol == arcade.key.A or symbol == arcade.key.S or symbol == arcade.key.D:
            self.keyboard_handler.set_key(symbol, True)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W or symbol == arcade.key.A or symbol == arcade.key.S or symbol == arcade.key.D:
            self.keyboard_handler.set_key(symbol, False)

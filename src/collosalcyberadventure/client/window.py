from collosalcyberadventure.client.keyboard import IKeyboardHandler
from typing import Final

import arcade


class IWindow:
    """Interface for the window class"""

    def setup(self):
        """Sets up window

        Sets up the game window. Called at the start of the game.

        Returns
        -------
        None
        """
        raise NotImplementedError("setup() method not implemented")

    def draw(self):
        """Draws the current frame

        Returns
        -------
        None
        """
        raise NotImplementedError("draw() method not implemented")

    def get_keyboard_handler(self) -> IKeyboardHandler:
        """

        Returns
        -------
        IKeyboardHandler
            class that handles all the keyboard logic
        """
        raise NotImplementedError("get_keyboard_handler() method not implemented")

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


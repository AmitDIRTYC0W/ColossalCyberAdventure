from collosalcyberadventure.client.keyboard import IKeyboardHandler


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

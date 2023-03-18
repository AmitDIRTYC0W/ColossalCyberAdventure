import arcade

from .login_screen import LoginScreenView
from . import constants


class ColossalCyberAdventure(arcade.Window):
    """Main window class. (0, 0) at the bottom left."""
    TITLE = "Colossal Cyber Adventure"
    BACKGROUND_COLOR = arcade.color.AMAZON

    def __init__(self):
        super().__init__(
            title=self.TITLE,
            vsync=constants.VSYNC,
            fullscreen=constants.FULLSCREEN,
        )
        self.background_color = self.BACKGROUND_COLOR

    def setup(self):
        """Set up window

        Sets up window. Call this again to restart game.
        """
        self.show_view(LoginScreenView())

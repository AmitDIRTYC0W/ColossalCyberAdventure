import arcade

from src.colossalcyberadventure.start_screen import StartScreenView


class ColossalCyberAdventure(arcade.Window):
    """Main window class. (0, 0) at the bottom left."""
    TITLE = "Colossal Cyber Adventure"
    BACKGROUND_COLOR = arcade.color.AMAZON

    def __init__(self):
        super().__init__(title=ColossalCyberAdventure.TITLE, fullscreen=True)

        arcade.set_background_color(ColossalCyberAdventure.BACKGROUND_COLOR)

    def setup(self):
        """Set up window

        Sets up window. Call this again to restart game.
        """

        self.show_view(StartScreenView())

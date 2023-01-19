import arcade
import arcade.gui

from colossalcyberadventure.game import GameView


class ColossalCyberAdventure(arcade.Window):
    """Main window class. (0, 0) at the bottom left."""
    TITLE = "Colossal Cyber Adventure"
    BACKGROUND_COLOR = arcade.color.AMAZON

    def __init__(self):
        super().__init__(title=ColossalCyberAdventure.TITLE, fullscreen=True)

        arcade.set_background_color(ColossalCyberAdventure.BACKGROUND_COLOR)

    def setupStartScreen(self):
        """Set up window

        Sets up window. Call this again to restart game.
        """

        self.show_view(StartScreenView())


class StartScreenView(arcade.View):
    """shows the view of the starting screen and lets you press the buttons"""

    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        @start_button.event("on_click")
        def on_click_settings(event):
            self.manager.clear()
            game_view = GameView()
            self.window.show_view(game_view)

        @settings_button.event("on_click")
        def on_click_settings(event):
            print("setting - insert here")

        @quit_button.event("on_click")
        def on_click_settings(event):
            arcade.exit()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()

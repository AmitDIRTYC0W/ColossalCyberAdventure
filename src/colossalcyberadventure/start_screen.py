import arcade
import arcade.gui

from colossalcyberadventure.game import GameView


class StartScreenView(arcade.View):
    """shows the view of the starting screen and lets you press the buttons"""

    BUTTON_WIDTH = 200
    BUTTON_BOTTOM = 20

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
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=StartScreenView.BUTTON_WIDTH)
        self.v_box.add(start_button.with_space_around(bottom=StartScreenView.BUTTON_BOTTOM))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=StartScreenView.BUTTON_WIDTH)
        self.v_box.add(settings_button.with_space_around(bottom=StartScreenView.BUTTON_BOTTOM))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=StartScreenView.BUTTON_WIDTH)
        self.v_box.add(quit_button.with_space_around(bottom=StartScreenView.BUTTON_BOTTOM))

        @start_button.event("on_click")
        def on_click_settings(_event):
            self.manager.clear()
            game_view = GameView()
            self.window.show_view(game_view)

        @settings_button.event("on_click")
        def on_click_settings(_event):
            print("setting - insert here")

        @quit_button.event("on_click")
        def on_click_settings(_event):
            arcade.exit()

        # centers the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()

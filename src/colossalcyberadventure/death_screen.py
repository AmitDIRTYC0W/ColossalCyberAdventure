import arcade
import arcade.gui


class DeathScreenView(arcade.View):
    """shows the view of the starting screen and lets you press the buttons"""

    BUTTON_WIDTH = 300
    BUTTON_LABEL_WIDTH = 80
    BUTTON_SPACING = 30

    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        restart_button = arcade.gui.UIFlatButton(
            text="restart",
            width=DeathScreenView.BUTTON_WIDTH
        )
        self.v_box.add(restart_button.with_border(width=1))

        quit_button = arcade.gui.UIFlatButton(
            text="Quit",
            width=DeathScreenView.BUTTON_WIDTH
        )
        self.v_box.add(quit_button.with_border(width=1))

        @restart_button.event("on_click")
        def on_click_settings(_event):
            from .game import GameView
            self.window.show_view(GameView())

        @quit_button.event("on_click")
        def on_click_settings(_event):
            arcade.exit()

        # centers the buttons
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.v_box
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_show_view(self):
        self.window.background_color = arcade.color.DARK_BLUE_GRAY
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

import arcade
import arcade.gui

from src.colossalcyberadventure.game import GameView


class StartScreenView(arcade.View):
    """shows the view of the starting screen and lets you press the buttons"""

    BUTTON_WIDTH = 200
    IP_LABEL_WIDTH = 30
    BUTTON_SPACING = 30

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
        # Create ip field
        ip_h_box = arcade.gui.UIBoxLayout(vertical=False)
        ip_label = arcade.gui.UILabel(text="IP: ", width=StartScreenView.IP_LABEL_WIDTH)
        ip_field = arcade.gui.UIInputText(width=StartScreenView.BUTTON_WIDTH, height=40)
        ip_h_box.add(ip_label)
        ip_h_box.add(ip_field)
        self.v_box.add(ip_h_box.with_border(width=1))

        connect_button = arcade.gui.UIFlatButton(text="Connect", width=StartScreenView.BUTTON_WIDTH)
        self.v_box.add(connect_button.with_border(width=1))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=StartScreenView.BUTTON_WIDTH)
        self.v_box.add(quit_button.with_border(width=1))

        @connect_button.event("on_click")
        def on_click_settings(_event):
            self.manager.clear()
            game_view = GameView()
            self.window.show_view(game_view)

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

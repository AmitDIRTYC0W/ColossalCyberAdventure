import arcade
import arcade.gui

import server.protocol
from src.colossalcyberadventure.start_screen import StartScreenView


class LoginScreenView(arcade.View):
    """shows the view of the starting screen and lets you press the buttons"""

    BUTTON_WIDTH = 200
    BUTTON_LABEL_WIDTH = 80
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
        username_h_box = arcade.gui.UIBoxLayout(vertical=False)
        username_label = arcade.gui.UILabel(text="Username: ", width=LoginScreenView.BUTTON_LABEL_WIDTH)
        username_field = arcade.gui.UIInputText(width=LoginScreenView.BUTTON_WIDTH, height=40)
        username_h_box.add(username_label)
        username_h_box.add(username_field)
        self.v_box.add(username_h_box.with_border(width=1))

        password_h_box = arcade.gui.UIBoxLayout(vertical=False)
        password_label = arcade.gui.UILabel(text="Password: ", width=LoginScreenView.BUTTON_LABEL_WIDTH)
        password_field = arcade.gui.UIInputText(width=LoginScreenView.BUTTON_WIDTH, height=40)
        password_h_box.add(password_label)
        password_h_box.add(password_field)
        self.v_box.add(password_h_box.with_border(width=1))

        login_button = arcade.gui.UIFlatButton(text="Login", width=LoginScreenView.BUTTON_WIDTH)
        self.v_box.add(login_button.with_border(width=1))

        register_button = arcade.gui.UIFlatButton(text="Register", width=LoginScreenView.BUTTON_WIDTH)
        self.v_box.add(register_button.with_border(width=1))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=LoginScreenView.BUTTON_WIDTH)
        self.v_box.add(quit_button.with_border(width=1))

        @login_button.event("on_click")
        def on_click_settings(_event):
            server.protocol.create_identification_request(username_field.text, password_field.text, False)
            self.manager.clear()
            start_view = StartScreenView()
            self.window.show_view(start_view)

        @register_button.event("on_click")
        def on_click_settings(_event):
            server.protocol.create_identification_request(username_field.text, password_field.text, True)

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

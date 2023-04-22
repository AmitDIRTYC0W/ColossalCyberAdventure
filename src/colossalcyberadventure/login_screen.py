import socket

import arcade
import arcade.gui

from colossalcyberadventure import constants
from colossalcyberadventure.game import GameView
from colossalcyberadventure.server.messages import create_identification_request, read_identification_response
from colossalcyberadventure.server_game_view import ServerGameView


class LoginScreenView(arcade.View):
    """shows the view of the starting screen and lets you press the buttons"""

    BUTTON_WIDTH = 300
    BUTTON_LABEL_WIDTH = 80
    BUTTON_SPACING = 30

    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()

        # Set background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create ip field
        ip_h_box = arcade.gui.UIBoxLayout(vertical=False)
        ip_label = arcade.gui.UILabel(text="IP: ", width=LoginScreenView.BUTTON_LABEL_WIDTH)
        self.ip_field = arcade.gui.UIInputText(width=LoginScreenView.BUTTON_WIDTH, height=40)
        ip_h_box.add(ip_label)
        ip_h_box.add(self.ip_field)
        self.v_box.add(ip_h_box.with_border(width=0.9))

        username_h_box = arcade.gui.UIBoxLayout(vertical=False)
        username_label = arcade.gui.UILabel(text="Username: ", width=LoginScreenView.BUTTON_LABEL_WIDTH)
        self.username_field = arcade.gui.UIInputText(width=LoginScreenView.BUTTON_WIDTH, height=40)
        username_h_box.add(username_label)
        username_h_box.add(self.username_field)
        self.v_box.add(username_h_box.with_border(width=1))

        password_h_box = arcade.gui.UIBoxLayout(vertical=False)
        password_label = arcade.gui.UILabel(text="Password: ", width=LoginScreenView.BUTTON_LABEL_WIDTH)
        self.password_field = arcade.gui.UIInputText(width=LoginScreenView.BUTTON_WIDTH, height=40)
        password_h_box.add(password_label)
        password_h_box.add(self.password_field)
        self.v_box.add(password_h_box.with_border(width=1))

        login_button = arcade.gui.UIFlatButton(text="Login", width=LoginScreenView.BUTTON_WIDTH)
        self.v_box.add(login_button.with_border(width=1))

        register_button = arcade.gui.UIFlatButton(text="Register", width=LoginScreenView.BUTTON_WIDTH)
        self.v_box.add(register_button.with_border(width=1))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=LoginScreenView.BUTTON_WIDTH)
        self.v_box.add(quit_button.with_border(width=1))

        @login_button.event("on_click")
        def on_click_login(_event):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip_field.text, constants.SERVER_PORT))
            s.send(
                create_identification_request(self.username_field.text, self.password_field.text, False)
                .to_bytes_packed()
            )
            response = read_identification_response(s.recv(constants.BUFFER_SIZE))
            match response.which():
                case "success":
                    self.manager.clear()
                    game_view = ServerGameView(s, response.success.playerid, response.success.coinamount,
                                               response.success.xpamount, response.success.mushroomamount,
                                               response.success.hpamount)
                    self.window.show_view(game_view)
                case "failure":
                    pass

        @register_button.event("on_click")
        def on_click_register(_event):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip_field.text, constants.SERVER_PORT))
            request = create_identification_request(self.username_field.text, self.password_field.text, True)
            s.send(request.to_bytes_packed())
            response = read_identification_response(s.recv(constants.BUFFER_SIZE))
            match response.which():
                case "success":
                    self.manager.clear()
                    game_view = ServerGameView(s, response.success.playerid, response.success.coinamount,
                                               response.success.xpamount, response.success.mushroomamount,
                                               response.success.hpamount)
                    self.window.show_view(game_view)
                case "failure":
                    pass

        @quit_button.event("on_click")
        def on_click_quit(_event):
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
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

import asyncio
from typing import cast

import arcade
import arcade.gui
from aioquic.asyncio import connect

from src.colossalcyberadventure.constants import SERVER_PORT
from src.colossalcyberadventure.server.connection import CONFIGURATION
from src.colossalcyberadventure.server.protocol import IdentificationProtocol
from src.colossalcyberadventure.login_screen import LoginScreenView


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
        self.ip_field = arcade.gui.UIInputText(width=StartScreenView.BUTTON_WIDTH, height=40)
        ip_h_box.add(ip_label)
        ip_h_box.add(self.ip_field)
        self.v_box.add(ip_h_box.with_border(width=1))

        connect_button = arcade.gui.UIFlatButton(text="Connect", width=StartScreenView.BUTTON_WIDTH)
        self.v_box.add(connect_button.with_border(width=1))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=StartScreenView.BUTTON_WIDTH)
        self.v_box.add(quit_button.with_border(width=1))

        @connect_button.event("on_click")
        def on_click_connect(_event):
            asyncio.run(self.handle_server())
            self.manager.clear()
            start_view = LoginScreenView()
            self.window.show_view(start_view)

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

    async def handle_server(self):
        async with connect("10.0.0.11", SERVER_PORT, configuration=CONFIGURATION,
                           create_protocol=IdentificationProtocol) as client:
            print("hi")
            client = cast(IdentificationProtocol, client)
            await client.send_identification("hi", "hi", False)


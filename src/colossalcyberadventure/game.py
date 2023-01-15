import arcade
import arcade.gui
from arcade import key as k

from colossalcyberadventure.camera import GameCam
from colossalcyberadventure.player import Player
from constants import *


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

class GameView(arcade.View):
    """View of the actual game

    Attributes
    ----------
    player: Player
    keyboard_state: dict[int, bool]
    map: arcade.tilemap.TileMap
        The full map
    scene: arcade.scene.Scene
    """

    BACKGROUND_COLOR = arcade.color.JET
    MAP_PATH = "resources/map/map.tmj"

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.keyboard_state = {k.W: False, k.A: False, k.S: False, k.D: False}
        self.camera = GameCam(self.window.width, self.window.height, self.player)
        self.map = arcade.load_tilemap(GameView.MAP_PATH, TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.map)

        arcade.set_background_color(GameView.BACKGROUND_COLOR)

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()
        self.player.draw()

    def on_update(self, delta_time: float):
        self.player.update_player_speed(self.keyboard_state)
        self.player.update_animation()
        self.player.update()
        self.camera.center_camera_on_player()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = True

    def on_key_release(self, symbol: int, _modifiers: int):
        if symbol in self.keyboard_state.keys():
            self.keyboard_state[symbol] = False


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

        start_button.on_click = self.on_click_start
        quit_button.on_click = self.on_click_quit
        settings_button.on_click = self.on_click_settings


        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    # defining the action of each button:
    def on_click_quit(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()

    def on_click_settings(self, event: arcade.gui.UIOnClickEvent):
        print("setting - insert here")

    def on_click_start(self, event: arcade.gui.UIOnClickEvent):
        game_view = GameView()
        self.window.show_view(game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()



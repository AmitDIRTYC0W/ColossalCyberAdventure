import arcade
import asyncio

from interruptingcow import timeout

from collosalcyberadventure.client.window import Window


def test_window_initialization():
    """Opens the window for 3 seconds

    Raises
    ------
    AssertionError:
        If the program exits before 3 seconds have passed

    """
    try:
        with timeout(3, asyncio.CancelledError):
            window = Window(800, 600, "test window", arcade.color.TAN)
            window.setup()
            window.run()
            assert False
    except asyncio.CancelledError:
        assert True

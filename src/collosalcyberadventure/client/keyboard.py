import arcade.key


class IKeyboardHandler:
    """This class holds all the key logic"""
    def get_pressed_keys(self) -> dict[int, bool]:
        raise NotImplementedError("get_pressed_keys() method not implemented")

from arcade import key as k


class IKeyboardHandler:
    """This class holds all the key logic"""
    def get_pressed_keys(self) -> dict[int, bool]:
        raise NotImplementedError("get_pressed_keys() method not implemented")

    def set_key(self, key: int, value: bool):
        raise NotImplementedError("set_key() method not implemented")


class KeyboardHandler(IKeyboardHandler):
    def __init__(self):
        self.pressed_keys = {k.W: False, k.A: False, k.S: False, k.D: False}

    def get_pressed_keys(self) -> dict[int, bool]:
        return self.pressed_keys

    def set_key(self, key: int, value: bool):
        if key in self.pressed_keys.keys():
            self.pressed_keys[key] = value

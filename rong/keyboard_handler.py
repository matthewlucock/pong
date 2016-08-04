from rong import event_names
from rong.window import window

class KeyboardHandler:
    ESCAPE_SYMBOL = "Escape"

    def __keypress_calback(self, event):
        key_symbol = event.keysym.lower()

        if key_symbol not in self.pressed_keys:
            self.pressed_keys.append(key_symbol)

    def __keyrelease_callback(self, event):
        key_symbol = event.keysym.lower()

        if key_symbol in self.pressed_keys:
            self.pressed_keys.remove(key_symbol)

    def __init__(self):
        self.pressed_keys = []

    def bind(self):
        self._keypress_calback_id = window.bind(
            event_names.KEYPRESS,
            self.__keypress_calback,
            add=True
        )
        self._keyrelease_calback_id = window.bind(
            event_names.KEYRELEASE,
            self.__keyrelease_callback,
            add=True
        )

    def unbind(self):
        self.pressed_keys = []
        window.unbind(event_names.KEYPRESS, self._keypress_calback_id)
        window.unbind(event_names.KEYRELEASE, self._keyrelease_calback_id)
        self._keypress_calback_id = None
        self._keyrelease_calback_id = None

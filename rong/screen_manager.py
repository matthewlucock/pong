import tkinter

class _ScreenManager:
    def __init__(self):
        self._current_screen = None
        self._previous_screen = None
        self.main_screen = None
        self.game_screen = None

    def change_screen(self, screen_to_change_to):
        if self._current_screen:
            self._current_screen.pack_forget()

        screen_to_change_to.pack(expand=True, fill=tkinter.BOTH)

        self._previous_screen = self._current_screen
        self._current_screen = screen_to_change_to

    def back(self):
        self.change_screen(self._previous_screen)

screen_manager = _ScreenManager()

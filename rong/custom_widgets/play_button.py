from rong import game_variables, event_names
from rong.window import window
from rong.screen_manager import screen_manager
from rong.game import Game
from .styled_button import StyledButton


class PlayButton(StyledButton):
    _TEXT = "Play"

    def __click_callback(self, *args):
        game_variables.game_mode.set(self.game_mode)
        screen_manager.change_screen(screen_manager.game_screen)
        window.update()
        current_game = Game()

    def __init__(self, master, game_mode=None):
        super().__init__(master=master, text=self._TEXT)

        self.game_mode = game_mode
        self.bind(event_names.LEFT_CLICK, self.__click_callback)

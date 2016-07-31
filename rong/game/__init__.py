from rong import game_variables, event_names, game_modes
from rong.window import window
from rong.keyboard_handler import KeyboardHandler
from .clock import Clock
from .paddle import Paddle
from .zen_wall import ZenWall
from .ball import Ball


class Game:
    __PADDLE_MARGIN_FROM_EDGE_OF_SCREEN = 75
    current_game = None

    def __init__(self, canvas):
        self._canvas = canvas

        window.update()

        self._ball = Ball(canvas=canvas)
        self._player_one_paddle = Paddle(canvas=canvas)

        if game_variables.game_mode.get() == game_modes.ZEN:
            self._zen_wall = ZenWall(canvas=canvas)
        else:
            self._player_two_paddle = Paddle(canvas=canvas, in_right_half=True)

            if game_variables.game_mode.get() != game_modes.MULTIPLAYER:
                #self._ai = AI(ball=ball, paddle=self._player_two_paddle)
                pass

        self._keyboard_handler = KeyboardHandler()
        self._clock = Clock()

        Game.current_game = self
        self.resume()

    def pause(self):
        game_variables.game_is_paused.set(True)
        self._keyboard_handler.unbind()

    def resume(self):
        game_variables.game_is_paused.set(False)
        self._keyboard_handler.bind()
        self._clock.update()

        while True:
            if (
                    game_variables.application_has_exited.get() \
                    or game_variables.game_is_paused.get()
            ):
                break

            self.update()
            self._clock.update()
            window.update()

    def update(self):
        delta_time = self._clock.calculate_delta_time()

        self._player_one_paddle.update_position(
            delta_time=delta_time,
            pressed_keys=self._keyboard_handler.pressed_keys
        )

        if game_variables.game_mode.get() != game_modes.ZEN:
            self._player_two_paddle.update_position(
                delta_time=delta_time,
                pressed_keys=self._keyboard_handler.pressed_keys
            )

        self._ball.update_position(delta_time=delta_time)

    def destroy(self):
        self._player_one_paddle.delete()
        self._ball.delete()

        if game_variables.game_mode.get() == game_modes.ZEN:
            self._zen_wall.delete()
        else:
            self._player_two_paddle.delete()

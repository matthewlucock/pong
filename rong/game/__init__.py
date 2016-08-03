from rong import game_variables, event_names, game_modes, utilities
from rong.window import window
from rong.keyboard_handler import KeyboardHandler
from .clock import Clock
from .paddle import Paddle
from .zen_wall import ZenWall
from .ball import Ball
from .ai import AI
from .power_up import Power_Up
import time, random

class Game:
    __MEAN_POWER_UP_TIME = 10
    __POWER_UP_TIME_DEVIATION = 2

    __PADDLE_MARGIN_FROM_EDGE_OF_SCREEN = 75
    SCORE_LIMIT = 10
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
                self._ai = AI(
                    ball=self._ball,
                    paddle=self._player_two_paddle,
                    difficulty = game_variables.versus_ai_difficulty.get()
                )

        self._top_interval = (
            utilities.Vector(0, 0),
            utilities.Vector(self._canvas.winfo_width(), 0)
        )
        self._bottom_interval = (
            utilities.Vector(0, self._canvas.winfo_height()),
            utilities.Vector(
                self._canvas.winfo_width(),
                self._canvas.winfo_height()
            )
        )

        self._power_ups = []
        self._active_effects = []
        self._next_power_up_time = self._get_new_power_up_time()

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
        if time.time() > self._next_power_up_time:
            self._power_ups.append(Power_Up(self._canvas))
            self._next_power_up_time = self._get_new_power_up_time()

        delta_time = self._clock.calculate_delta_time()

        self._player_one_paddle.update_position(
            delta_time=delta_time,
            pressed_keys=self._keyboard_handler.pressed_keys
        )

        if game_variables.game_mode.get() == game_modes.MULTIPLAYER:
            self._player_two_paddle.update_position(
                delta_time=delta_time,
                pressed_keys=self._keyboard_handler.pressed_keys
            )
        elif game_variables.game_mode.get() == game_modes.VERSUS_AI:
            self._ai.move(delta_time)

        intervals = [self._top_interval, self._bottom_interval] + list(self._player_one_paddle._intervals)
        if game_variables.game_mode.get() == game_modes.ZEN:
            intervals.append(self._zen_wall._interval)
        else:
            intervals += list(self._player_two_paddle._intervals)

        self._ball.update_position(delta_time, intervals)

    def destroy(self):
        if not game_variables.game_is_paused.get():
            self.pause()

        self._player_one_paddle.delete()
        self._ball.delete()

        if game_variables.game_mode.get() == game_modes.ZEN:
            self._zen_wall.delete()
        else:
            self._player_two_paddle.delete()

        game_variables.player_one_score.set(0)
        game_variables.player_two_score.set(0)
        game_variables.game_is_paused.set(False)

    def _get_new_power_up_time(self):
        return time.time() + random.gauss(
            self.__MEAN_POWER_UP_TIME,
            self.__POWER_UP_TIME_DEVIATION
        )

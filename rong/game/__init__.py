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
    __MEAN_POWER_UP_TIME = 4
    __POWER_UP_TIME_DEVIATION = 2

    _ball_vertical_limit = 20

    __PADDLE_MARGIN_FROM_EDGE_OF_SCREEN = 75
    SCORE_LIMIT = 10
    current_game = None
    canvas = None
    score_label = None
    open_pause_menu = None
    close_pause_menu = None

    def __window_movement_and_focus_loss_listener(self, *args):
        if self._first_frame_has_been_processed:
            self.pause()
            Game.open_pause_menu()

    def __bind_window_movement_and_focus_loss_listeners(self):
        self._window_movement_listener_id = window.bind(
            event_names.CONFIGURE,
            self.__window_movement_and_focus_loss_listener
        )
        self._window_focus_loss_listener_id = window.bind(
            event_names.FOCUS_LOSS,
            self.__window_movement_and_focus_loss_listener
        )

    def __unbind_window_movement_and_focus_loss_listeners(self):
        window.unbind(event_names.CONFIGURE, self._window_movement_listener_id)
        window.unbind(
            event_names.FOCUS_LOSS,
            self._window_focus_loss_listener_id
        )
        self._window_movement_listener_id = None
        self._window_focus_loss_listener_id = None

    def __escape_keypress_listener(self, event):
        if event.keysym != KeyboardHandler.ESCAPE_SYMBOL:
            return

        if game_variables.game_is_paused.get():
            Game.close_pause_menu()
            self.resume()
        else:
            self.pause()
            Game.open_pause_menu()

    def __bind_escape_keypress_listener(self):
        self._escape_keypress_listener_id = window.bind(
            event_names.KEYPRESS,
            self.__escape_keypress_listener,
            add=True
        )

    def __unbind_escape_keypress_listener(self):
        window.unbind(event_names.KEYPRESS, self._escape_keypress_listener_id)
        self._escape_kepress_listener_id = None

    def __init__(self):
        window.update()

        self._balls = [Ball(canvas=self.canvas)]
        self._player_one_paddle = Paddle(canvas=self.canvas)

        if game_variables.game_mode.get() == game_modes.ZEN:
            self._zen_wall = ZenWall(canvas=self.canvas)
        else:
            self._player_two_paddle = Paddle(
                canvas=self.canvas,
                in_right_half=True
            )

            if game_variables.game_mode.get() != game_modes.MULTIPLAYER:
                self._ai = AI(
                    balls=self._balls,
                    paddle=self._player_two_paddle,
                    difficulty = game_variables.versus_ai_difficulty.get()
                )

        self._top_interval = (
            utilities.Vector(0, 0),
            utilities.Vector(self.canvas.winfo_width(), 0)
        )
        self._bottom_interval = (
            utilities.Vector(0, self.canvas.winfo_height()),
            utilities.Vector(
                self.canvas.winfo_width(),
                self.canvas.winfo_height()
            )
        )

        self._power_ups = []
        self._active_effects = []
        self._next_power_up_time = self._get_new_power_up_time()

        game_variables.player_one_score.set(0)
        game_variables.player_two_score.set(0)

        if game_variables.game_mode.get() == game_modes.ZEN:
            Game.score_label.pack_forget()
        else:
            Game.score_label.pack()

        Ball.set_score_label()
        self._first_frame_has_been_processed = False

        self._keyboard_handler = KeyboardHandler()
        self.__bind_escape_keypress_listener()

        self._clock = Clock()
        Game.current_game = self

        self.resume()

    def pause(self):
        game_variables.game_is_paused.set(True)
        self.__unbind_window_movement_and_focus_loss_listeners()

    def resume(self):
        game_variables.game_is_paused.set(False)
        self._keyboard_handler.bind()
        self.__bind_window_movement_and_focus_loss_listeners()
        self._clock.calculate_delta_time()

        while True:
            if (
                    game_variables.application_has_exited.get() \
                    or game_variables.game_is_paused.get()
            ):
                break

            self.update()
            window.update()
            self._first_frame_has_been_processed = True

    def update(self):
        delta_time = self._clock.calculate_delta_time()

        if (
                game_variables.power_ups_enabled.get()
                and game_variables.game_mode.get() != game_modes.ZEN
        ):
            for effect in self._active_effects:
                if time.time() >= effect[1]:
                    self._remove_effect(effect)
                    self._active_effects.remove(effect)
            for power_up in self._power_ups:
                for ball in self._balls:
                    if (
                                ball.collides_with_power_up(power_up)
                                and ball.last_hit_by
                        ):
                        self._active_effects.append(
                            (
                                power_up.effect,
                                time.time() + power_up.EFFECT_DURATION,
                                ball.last_hit_by
                            )
                        )
                        self._apply_effect(power_up.effect, ball.last_hit_by)
                        self._power_ups.remove(power_up)
                        power_up.delete()
                if time.time() >= power_up.end_time:
                    self._power_ups.remove(power_up)
                    power_up.delete()
            if time.time() > self._next_power_up_time:
                self._power_ups.append(Power_Up(self.canvas))
                self._next_power_up_time = self._get_new_power_up_time()

        effects = []
        for effect in self._active_effects:
            effects.append(effect[0])

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

        for ball in self._balls:
            ball.update_position(delta_time, intervals)

        for ball in self._balls:
            if (
                    ball.position.y < -self._ball_vertical_limit
                    or ball.position.y > self.canvas.winfo_height() + self._ball_vertical_limit
            ):
                ball.reset()

    def destroy(self):
        self.pause()
        self._keyboard_handler.unbind()
        self.__unbind_escape_keypress_listener()

        self._player_one_paddle.delete()

        for ball in self._balls:
            ball.delete()

        for power_up in self._power_ups:
            power_up.delete()
        self._power_ups = []
        for effect in self._active_effects:
            self._remove_effect(effect)
        self._active_effects = []

        if game_variables.game_mode.get() == game_modes.ZEN:
            self._zen_wall.delete()
        else:
            self._player_two_paddle.delete()

        game_variables.game_is_paused.set(False)

    def _get_new_power_up_time(self):
        return time.time() + utilities.larger_than_zero_gaussian(
            self.__MEAN_POWER_UP_TIME,
            self.__POWER_UP_TIME_DEVIATION
        )

    def _apply_effect(self, effect, player):
        if effect == Power_Up.MULTIPLE_BALLS:
            self._balls.append(Ball(canvas = self.canvas))
        elif effect == Power_Up.BALL_SPEED_BOOST:
            Ball.velocity_multiplier *= 2
        elif effect == Power_Up.BALL_SPEED_REDUCTION:
            Ball.velocity_multiplier /= 2
        elif effect == Power_Up.ENGORGEMENT:
            Ball.radius_multiplier *= 2
        elif effect == Power_Up.ENSMALLMENT:
            Ball.radius_multiplier /= 2
        elif effect == Power_Up.OWN_PADDLE_SPEED_BOOST:
            if player == 1:
                self._player_one_paddle.velocity_multiplier *= 2
            elif player == 2:
                self._player_two_paddle.velocity_multiplier *= 2
        elif effect == Power_Up.OTHER_PADDLE_SPEED_REDUCTION:
            if player == 1:
                self._player_two_paddle.velocity_multiplier /= 2
            elif player == 2:
                self._player_one_paddle.velocity_multiplier /= 2
        elif effect == Power_Up.SELF_WIDENMENT:
            if player == 1:
                self._player_one_paddle.height_multiplier *= 2
            elif player == 2:
                self._player_two_paddle.height_multiplier *= 2
        elif effect == Power_Up.OTHER_NARROWMENT:
            if player == 1:
                self._player_two_paddle.height_multiplier /= 2
            elif player == 2:
                self._player_one_paddle.height_multiplier /= 2
        elif effect == Power_Up.LOCK_OPPONENT_ROTATION:
            if player == 1:
                self._player_two_paddle.can_rotate = False
            elif player == 2:
                self._player_one_paddle.can_rotate = False
        elif effect == Power_Up.LOCK_OPPONENT_POSITION:
            if player == 1:
                self._player_two_paddle.can_move = False
            elif player == 2:
                self._player_one_paddle.can_move = False

    def _remove_effect(self, effect):
        if effect[0] == Power_Up.MULTIPLE_BALLS:
            self._balls[1].delete()
            self._balls.pop(1)
        elif effect[0] == Power_Up.BALL_SPEED_BOOST:
            Ball.velocity_multiplier /= 2
        elif effect[0] == Power_Up.UBER_BALL_SPEED_BOOST:
            Ball.velocity_multiplier /= 4
        elif effect[0] == Power_Up.BALL_SPEED_REDUCTION:
            Ball.velocity_multiplier *= 2
        elif effect[0] == Power_Up.ENGORGEMENT:
            Ball.radius_multiplier /= 2
        elif effect[0] == Power_Up.ENSMALLMENT:
            Ball.radius_multiplier *= 2
        elif effect[0] == Power_Up.OWN_PADDLE_SPEED_BOOST:
            if effect[2] == 1:
                self._player_one_paddle.velocity_multiplier /= 2
            elif effect[2] == 2:
                self._player_two_paddle.velocity_multiplier /= 2
        elif effect[0] == Power_Up.OTHER_PADDLE_SPEED_REDUCTION:
            if effect[2] == 1:
                self._player_two_paddle.velocity_multiplier *= 2
            elif effect[2] == 2:
                self._player_one_paddle.velocity_multiplier *= 2
        elif effect[0] == Power_Up.SELF_WIDENMENT:
            if effect[2] == 1:
                self._player_one_paddle.height_multiplier /= 2
            elif effect[2] == 2:
                self._player_two_paddle.height_multiplier /= 2
        elif effect[0] == Power_Up.OTHER_NARROWMENT:
            if effect[2] == 1:
                self._player_two_paddle.height_multiplier *= 2
            elif effect[2] == 2:
                self._player_one_paddle.height_multiplier *= 2
        elif effect[0] == Power_Up.LOCK_OPPONENT_ROTATION:
            if effect[2] == 1:
                self._player_two_paddle.can_rotate = True
            elif effect[2] == 2:
                self._player_one_paddle.can_rotate = True
        elif effect[0] == Power_Up.LOCK_OPPONENT_POSITION:
            if effect[2] == 1:
                self._player_two_paddle.can_move = True
            elif effect[2] == 2:
                self._player_one_paddle.can_move = True

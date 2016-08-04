import random
from rong import utilities
import time

class Power_Up:
    RADIUS = 25
    EFFECT_DURATION = 5
    __MEAN_ON_SCREEN_DURATION = 10
    __ON_SCREEN_DURATION_DEVIATION = 2
    __MIN_FRACTIONAL_X = 0.1
    __MAX_FRACTIONAL_X = 0.9
    __MIN_FRACTIONAL_Y = 0.1
    __MAX_FRACTIONAL_Y = 0.9

    MULTIPLE_BALLS = "multiple_balls"
    BALL_SPEED_BOOST = "ball_speed_boost"
    UBER_BALL_SPEED_BOOST = "uber_ball_speed_boost"
    BALL_SPEED_REDUCTION = "ball_speed_reduction"
    ENGORGEMENT = "engorgement"
    ENSMALLMENT = "ensmallment"
    OWN_PADDLE_SPEED_BOOST = "own_paddle_speed_boost"
    OTHER_PADDLE_SPEED_REDUCTION = "other_paddle_speed_reduction"
    SELF_WIDENMENT = "self_widenment"
    OTHER_NARROWMENT = "other_narrowment"
    LOCK_OPPONENT_ROTATION = "lock_opponent_rotation"
    LOCK_OPPONENT_POSITION = "lock_opponent_position"

    _EFFECTS = [
        MULTIPLE_BALLS,
        BALL_SPEED_BOOST,
        UBER_BALL_SPEED_BOOST,
        BALL_SPEED_REDUCTION,
        ENGORGEMENT,
        ENSMALLMENT,
        OWN_PADDLE_SPEED_BOOST,
        OTHER_PADDLE_SPEED_REDUCTION,
        SELF_WIDENMENT,
        OTHER_NARROWMENT,
        LOCK_OPPONENT_ROTATION,
        LOCK_OPPONENT_POSITION
    ]
    _COLOURS = [
        "red",
        "green",
        "blue",
        "yellow",
        "red",
        "green",
        "blue",
        "yellow",
        "red",
        "green",
        "blue",
        "yellow"
    ]

    def __init__(self, canvas):
        min_x = canvas.winfo_width() * self.__MIN_FRACTIONAL_X
        max_x = canvas.winfo_width() * self.__MAX_FRACTIONAL_X
        min_y = canvas.winfo_height() * self.__MIN_FRACTIONAL_Y
        max_y = canvas.winfo_height() * self.__MAX_FRACTIONAL_Y
        self.position = utilities.Vector(
            min_x + random.random() * (max_x - min_x),
            min_y + random.random() * (max_y - min_y)
        )

        self._type = random.randint(1, len(self._EFFECTS)) - 1

        self.effect = self._EFFECTS[self._type]

        duration = utilities.larger_than_zero_gaussian(
            self.__MEAN_ON_SCREEN_DURATION,
            self.__ON_SCREEN_DURATION_DEVIATION
        )

        self.end_time = time.time() + duration

        self._canvas = canvas

        self._canvas_id = canvas.create_oval(
            *utilities.get_canvas_circle_coordinates(
                centre=self.position,
                radius=self.RADIUS
            ),
            width=0,
            fill=self._COLOURS[self._type]
        )

    def delete(self):
        self._canvas.delete(self._canvas_id)
import random
from rong import utilities

class Power_Up:
    RADIUS = 15
    __MIN_FRACTIONAL_X = 0.1
    __MAX_FRACTIONAL_X = 0.9
    __MIN_FRACTIONAL_Y = 0.1
    __MAX_FRACTIONAL_Y = 0.9

    _SPEED_UP_GAME = "speed_up_game"
    _SLOW_DOWN_GAME = "slow_down_game"
    _LOCK_OPPONENT_ROTATION = "lock_opponent_rotation"
    _LOCK_OPPONENT_POSITION = "lock_opponent_position"
    _EFFECTS = [
        _SPEED_UP_GAME,
        _SLOW_DOWN_GAME,
        _LOCK_OPPONENT_ROTATION,
        _LOCK_OPPONENT_POSITION
    ]

    def __init__(self, canvas):
        self.position = utilities.Vector(
            random.randrange(
                canvas.winfo_width() * self.__MIN_FRACTIONAL_X,
                canvas.winfo_width() * self.__MAX_FRACTIONAL_X
            ),
            random.randrange(
                canvas.winfo_height() * self.__MIN_FRACTIONAL_Y,
                canvas.winfo_height() * self.__MAX_FRACTIONAL_Y
            )
        )
        self.effect = self._EFFECTS[random.randint(1, len(self._EFFECTS)) - 1]
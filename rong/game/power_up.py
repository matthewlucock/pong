import random
from rong import utilities

class Power_Up:
    RADIUS = 15
    DURATION = 5
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
        min_x = canvas.winfo_width() * self.__MIN_FRACTIONAL_X
        max_x = canvas.winfo_width() * self.__MAX_FRACTIONAL_X
        min_y = canvas.winfo_height() * self.__MIN_FRACTIONAL_Y
        max_y = canvas.winfo_height() * self.__MAX_FRACTIONAL_Y
        self.position = utilities.Vector(
            min_x + random.random() * (max_x - min_x),
            min_y + random.random() * (max_y - min_y)
        )
        self.effect = self._EFFECTS[random.randint(1, len(self._EFFECTS)) - 1]
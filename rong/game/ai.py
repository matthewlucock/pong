from rong import utilities
import random

class AI:
    def __init__(self, ball, paddle, difficulty):
        self.ball = ball
        self.paddle = paddle
        self.difficulty = difficulty

        self.height = paddle.SIZE.y

        x_coord = paddle.position.x
        self.line = (
            utilities.Vector(x = x_coord),
            utilities.Vector(x_coord, 1)
        )

    def _predict_possition(self):
        try:
            correct_prediction = utilities.get_line_collision(
                self.ball._last_position,
                self.ball.position,
                *self.line
            )
        except ValueError:
            return
        standard_deviation = self.height * (-self.difficulty/6 + 13/6)
        prediction = utilities.Vector(
            correct_prediction.x,
            random.gauss(correct_prediction.y, standard_deviation)
        )
        return prediction

    def move(self, delta_time):
        prediction = self._predict_possition()
        if prediction:
            if prediction.y > self.paddle.position.y:
                self.paddle.update_position(
                    delta_time = delta_time,
                    pressed_keys = ("k")
                )
            elif prediction.y < self.paddle.position.y:
                self.paddle.update_position(
                    delta_time = delta_time,
                    pressed_keys = ("i")
                )
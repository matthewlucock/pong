from rong import utilities
import random

class AI:
    def __init__(self, balls, paddle, difficulty):
        self.balls = balls
        self.paddle = paddle
        self.difficulty = difficulty

        self.height = paddle.BASE_SIZE.y

        x_coord = paddle.position.x
        self.line = (
            utilities.Vector(x = x_coord),
            utilities.Vector(x_coord, 1)
        )

    def _predict_possition(self, ball):
        try:
            correct_prediction = utilities.get_line_collision(
                ball._last_position,
                ball.position,
                *self.line
            )
        except ValueError:
            return
        standard_deviation = self.height * (-self.difficulty + 10.5)#(-self.difficulty/2 + 5.5)#(-self.difficulty/4 + 3)#(-self.difficulty/6 + 13/6)
        prediction = utilities.Vector(
            correct_prediction.x,
            random.gauss(correct_prediction.y, standard_deviation)
        )
        return prediction

    def _get_closest_ball(self):
        closest_ball = self.balls[0]
        for ball in self.balls:
            if (ball.position - self.paddle.position).magnitude <= (closest_ball.position - self.paddle.position).magnitude:
                closest_ball = ball
        return closest_ball

    def move(self, delta_time):
        ball = self._get_closest_ball()
        prediction = self._predict_possition(ball)
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

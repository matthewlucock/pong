import random
from rong import utilities

class Ball:
    __BASE_RADIUS = 20
    __BACKGROUND_COLOR = "green"
    __VELOCITY_MULTIPLIER = 250

    def __generate_random_starting_velocity(self):
        velocity = utilities.Vector(1, random.random() * 2 - 1)
        velocity.normalise()

        if random.randint(0, 1):
            velocity *= -1

        velocity *= self.__VELOCITY_MULTIPLIER
        return velocity

    def __init__(self, canvas):
        self._canvas = canvas
        self.radius = self.__BASE_RADIUS

        self.position = utilities.Vector(
            canvas.winfo_width() / 2,
            canvas.winfo_height() / 2
        )

        self.velocity = self.__generate_random_starting_velocity()

        self._canvas_id = canvas.create_oval(
            *utilities.get_canvas_circle_coordinates(
                centre=self.position,
                radius=self.radius
            ),
            fill=self.__BACKGROUND_COLOR,
            width=0
        )

    def update_position(self, delta_time):
        movement = self.velocity * delta_time
        self.position += movement
        self.update_position_on_canvas()

    def update_position_on_canvas(self):
        self._canvas.coords(
            self._canvas_id,
            *utilities.get_canvas_circle_coordinates(
                centre=self.position,
                radius=self.radius
            )
        )

    def delete(self):
        self._canvas.delete(self._canvas_id)

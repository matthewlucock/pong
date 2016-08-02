import random, math
from rong import utilities

class Ball:
    __BASE_RADIUS = 20
    __BACKGROUND_COLOR = "green"
    __VELOCITY_MULTIPLIER = 250
    __A_LITTLE_BIT = 0.1

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

        self._last_position = self.position.copy()

        self.velocity = self.__generate_random_starting_velocity()

        self._canvas_id = canvas.create_oval(
            *utilities.get_canvas_circle_coordinates(
                centre=self.position,
                radius=self.radius
            ),
            fill=self.__BACKGROUND_COLOR,
            width=0
        )

    def update_position(self, delta_time, intervals):
        self._check_bounce(intervals)
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

    def collides_with_power_up(self, power_up):
        return (
            self.radius + power_up.radius <= (self.position - power_up.position).magnitude
        )

    def _check_bounce(self, intervals):
        for interval in intervals:
            #collided_between_frames = (self._collides_path(interval)
            #    or self._collides_corners(interval[0])
            #    or self._collides_corners(interval[1])
            #)
            if (
                    self._collides_now(interval)
            #        or collided_between_frames
            ):
                moving_towards = self.position + self.velocity
                point_of_collision = utilities.get_line_collision(self.position, moving_towards, *interval)
                if utilities.in_direction(
                        point_of_collision,
                        self.position,
                        self.velocity
                ):
                    polar_from_collision = self.position.get_polar_from_reference(
                        point_of_collision
                    )
                    polar_of_line = interval[0].get_polar_from_reference(
                        point_of_collision
                    )
                    smaller_line_angle = polar_of_line[1]
                    new_polar = (
                        polar_from_collision[0],
                        math.pi - polar_from_collision[1] + 2 * smaller_line_angle
                    )
                    location_of_direction_from_collision = utilities.Vector.point_at_polar_from_reference(
                        new_polar,
                        point_of_collision
                    )
                    new_velocity_direction = location_of_direction_from_collision - point_of_collision
                    self.velocity = new_velocity_direction.get_at_magnitude(
                        self.__VELOCITY_MULTIPLIER
                    )
            #        if collided_between_frames:
            #            new_displacement_from_collision = new_velocity_direction.get_at_magnitude(self.__A_LITTLE_BIT)
            #            self.position = point_of_collision + new_displacement_from_collision

    def _collides_now(self, interval):
        c = self.position
        r = self.radius
        m = interval[0]
        n = interval[1]
        v = n - m
        t = (v.x * c.x + v.y * c.y - v.x * m.x - v.y * m.y) / (v.x**2 + v.y**2)
        p = m + (v * t)
        if t <= 0:
            return ((c - m).magnitude <= r)
        elif t < 1:
            return ((c - p).magnitude <= r)
        else:
            return ((c - n).magnitude <= r)

    '''
    def _collides_path(self, interval):
        if self._last_position == self.position:
            return False

        point_of_collision = utilities.get_line_collision(
            self.position,
            self._last_position, 
            *interval
        )
        return (
            utilities.point_is_on_interval(
                point_of_collision,
                (self.position, self._last_position)
            )
            and utilities.point_is_on_interval(
                point_of_collision,
                interval
            )
        )

    def _collides_corners(self, corner):
        if self._last_position == self.position:
            return False

        c = corner
        r = self.radius
        m = self._last_position
        n = self.position
        v = n - m
        t = (v.x * c.x + v.y * c.y - v.x * m.x - v.y * m.y) / (v.x**2 + v.y**2)
        p = m + (v * t)
        if t <= 0:
            return ((c - m).magnitude <= r)
        elif t < 1:
            return ((c - p).magnitude <= r)
        else:
            return ((c - n).magnitude <= r)
    '''
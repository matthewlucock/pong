import random, math
from rong import utilities, colors, game_variables

class Ball:
    __BASE_RADIUS = 20
    __VELOCITY_MAGNITUDE = 700
    __OFF_SCREEN_DISTANCE_MULTIPLIER = 5
    radius_multiplier = 1
    velocity_multiplier = 1

    @property
    def radius(self):
        return self.__BASE_RADIUS * self.radius_multiplier


    def reset(self):
        self.position = utilities.Vector(
            self._canvas.winfo_width() / 2,
            self._canvas.winfo_height() / 2
        )
        self.velocity = self.__generate_random_starting_velocity()
        self.last_hit_by = 0

    def __generate_random_starting_velocity(self):
        velocity = utilities.Vector(1, random.random() * 2 - 1)
        velocity.normalise()

        if random.randint(0, 1):
            velocity *= -1

        velocity *= self.__VELOCITY_MAGNITUDE * self.velocity_multiplier
        return velocity

    def __ball_color_trace_callback(self, *args):
        self._canvas.itemconfig(self._canvas_id, fill=colors.ball.get())

    def __init__(self, canvas):
        self._canvas = canvas

        self.reset()
        self._last_position = self.position.copy()

        self._canvas_id = canvas.create_oval(
            *utilities.get_canvas_circle_coordinates(
                centre=self.position,
                radius=self.radius
            ),
            width=0,
        )

        self.__ball_color_trace_callback()
        self._ball_color_trace_observer_name = colors.ball.trace(
            "w",
            self.__ball_color_trace_callback
        )

    def update_position(self, delta_time, intervals):
        if (
                self.position.x
                < -self.radius * self.__OFF_SCREEN_DISTANCE_MULTIPLIER
        ):
            utilities.increment_tkinter_integer_variable(
                variable=game_variables.player_two_score
            )
            Ball.set_score_label()
            self.reset()
        elif (
                self.position.x > (
                    self._canvas.winfo_width()
                    + self.radius * self.__OFF_SCREEN_DISTANCE_MULTIPLIER
                )
        ):
            utilities.increment_tkinter_integer_variable(
                variable=game_variables.player_one_score
            )
            Ball.set_score_label()
            self.reset()

        self._check_bounce(intervals)
        movement = self.velocity.get_at_magnitude(
            delta_time * self.__VELOCITY_MAGNITUDE * self.velocity_multiplier
        )
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
        colors.ball.trace_vdelete("w", self._ball_color_trace_observer_name)

    def collides_with_power_up(self, power_up):
        return (
            self.radius + power_up.RADIUS >= (self.position - power_up.position).magnitude
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

                    index = intervals.index(interval)
                    if (
                            (index == 3 or index == 9)
                            and not game_variables.free_movement_enabled.get()
                    ):
                        new_polar = (
                            new_polar[0],
                            self._special_bounce(interval, point_of_collision, True if index == 9 else False)
                        )

                    location_of_direction_from_collision = utilities.Vector.point_at_polar_from_reference(
                        new_polar,
                        point_of_collision
                    )
                    new_velocity_direction = location_of_direction_from_collision - point_of_collision
                    self.velocity = new_velocity_direction.get_at_magnitude(
                        self.__VELOCITY_MAGNITUDE * self.velocity_multiplier
                    )
            #        if collided_between_frames:
            #            new_displacement_from_collision = new_velocity_direction.get_at_magnitude(self.__A_LITTLE_BIT)
            #            self.position = point_of_collision + new_displacement_from_collision
                    if 2 <= index <= 5:
                        self.last_hit_by = 1
                    elif 6 <= index <= 9:
                        self.last_hit_by = 2

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

    def _special_bounce(self, interval, point_of_collision, right_hand_side):
        midpoint = utilities.midpoint(interval[0], interval[1])
        distance_to_0 = (point_of_collision - interval[0]).magnitude
        distance_to_1 = (point_of_collision - interval[1]).magnitude
        distance_to_midpoint = (point_of_collision - midpoint).magnitude
        full_distance = (interval[0] - midpoint).magnitude

        if right_hand_side:
            if distance_to_0 <= distance_to_1:
                offset = distance_to_midpoint / full_distance
            elif distance_to_1 < distance_to_0:
                offset = -distance_to_midpoint / full_distance
            angle = math.pi + ((math.pi / 4) * offset)
        else:
            if distance_to_0 <= distance_to_1:
                offset = -distance_to_midpoint / full_distance
            elif distance_to_1 < distance_to_0:
                offset = distance_to_midpoint / full_distance
            angle = (math.pi / 4) * offset

        return angle

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

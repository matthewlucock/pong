import copy
from rong import directions, game_variables, utilities, colors

class Paddle:
    BASE_SIZE = utilities.Vector(30, 150)
    __BASE_DIAGONAL = BASE_SIZE / 2
    __BASE_SPEED = 700
    __ROTATION_RATE = 10
    __BOUNDARY_PADDING = 50

    __LEFT_HALF_KEYS = {
        "up": "w",
        "down": "s",
        "left": "a",
        "right": "d"
    }

    __RIGHT_HALF_KEYS = {
        "up": "i",
        "down": "k",
        "left": "j",
        "right": "l"
    }

    @property
    def diagonal(self):
        final = self.__BASE_DIAGONAL.copy()
        final.y *= self.height_multiplier
        return final    

    def __new_points(self, new_position):
        points = [
            new_position + self.diagonal.inverted,
            new_position + self.diagonal.inverted_y,
            new_position + self.diagonal,
            new_position + self.diagonal.inverted_x
        ]

        new_points = []
        for point in points:
            polar = point.get_polar_from_reference(new_position)
            polar = (polar[0], polar[1] + self.rotation)
            point = utilities.Vector.point_at_polar_from_reference(polar, new_position)
            new_points.append(point)

        return new_points

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        new_position = copy.deepcopy(new_position)

        points = self.__new_points(new_position)

        for point in points:
            for boundary in self._boundaries:
                if not utilities.point_is_on_this_side_of_interval(
                        self.position,
                        point,
                        boundary
                ):
                    correction = utilities.vector_to_line(point, boundary)
                    new_position += correction
                    points = self.__new_points(new_position)

        self._position = new_position
        self._top_left_vertex = points[0]
        self._top_right_vertex = points[1]
        self._bottom_right_vertex = points[2]
        self._bottom_left_vertex = points[3]

        self._intervals = [
            (self._top_left_vertex, self._top_right_vertex),
            (self._top_right_vertex, self._bottom_right_vertex),
            (self._bottom_left_vertex, self._bottom_right_vertex),
            (self._top_left_vertex, self._bottom_left_vertex)
        ]

    def __get_polygon_coordinates(self):
        return (
            self._top_left_vertex.tuple \
            + self._top_right_vertex.tuple \
            + self._bottom_right_vertex.tuple \
            + self._bottom_left_vertex.tuple
        )

    def __paddle_color_trace_callback(self, *args):
        self._canvas.itemconfig(self._canvas_id, fill=colors.paddle.get())

    def __init__(self, canvas, in_right_half=False):
        self.velocity_multiplier = 1
        self.height_multiplier = 1
        self.can_move = True
        self.can_rotate = True

        self._canvas = canvas
        self._in_right_half = in_right_half

        self._canvas_size = utilities.Vector(
            canvas.winfo_width(),
            canvas.winfo_height()
        )

        x_offset = self.__BOUNDARY_PADDING + self.BASE_SIZE.x / 2
        if in_right_half:
            x_offset = (
                self._canvas_size.x
                - self.__BOUNDARY_PADDING
                - self.BASE_SIZE.x / 2
            )

        self._boundaries = [
            (utilities.Vector(), self._canvas_size.x_component),
            (self._canvas_size.y_component, self._canvas_size)
        ]

        if in_right_half:
            middle_boundary_x = self._canvas_size.x / 2 + self.__BOUNDARY_PADDING
            self._boundaries.append(
                (self._canvas_size.x_component, self._canvas_size)
            )
            self._boundaries.append(
                (
                    utilities.Vector(x = middle_boundary_x),
                    utilities.Vector(
                        middle_boundary_x,
                        self._canvas_size.y
                    )
                )
            )
        else:
            middle_boundary_x = self._canvas_size.x / 2 - self.__BOUNDARY_PADDING
            self._boundaries.append(
                (utilities.Vector(), self._canvas_size.y_component)
            )
            self._boundaries.append(
                (
                    utilities.Vector(x = middle_boundary_x),
                    utilities.Vector(
                        middle_boundary_x,
                        self._canvas_size.y
                    )
                )
            )

        self.rotation = 0

        self._position = utilities.Vector(
            x_offset,
            self._canvas_size.y / 2
        )

        self.position = utilities.Vector(
            x_offset,
            self._canvas_size.y / 2
        )

        self._canvas_id = canvas.create_polygon(
            *self.__get_polygon_coordinates(),
        )

        self.__paddle_color_trace_callback()
        self._paddle_color_trace_observer_name = colors.paddle.trace(
            "w",
            self.__paddle_color_trace_callback
        )

    def update_position(self, delta_time, pressed_keys):
        frame_speed = self.__BASE_SPEED * self.velocity_multiplier * delta_time
        frame_rotation = self.__ROTATION_RATE * self.velocity_multiplier * delta_time

        direction = directions.get_direction_from_keys(
            keys=pressed_keys,
            in_right_half=self._in_right_half
        )

        rotation_increment = directions.get_rotation_from_keys(
            keys = pressed_keys,
            in_right_half = self._in_right_half
        )

        if not game_variables.free_movement_enabled.get():
            direction.x = 0
            direction.normalise()
            rotation_increment = 0

        velocity = direction * frame_speed

        self.rotation += rotation_increment * frame_rotation * self.can_rotate
        self.position += velocity * self.can_move
        self.update_position_on_canvas()

    def update_position_on_canvas(self):
        self._canvas.coords(
            self._canvas_id,
            *self.__get_polygon_coordinates()
        )

    def delete(self):
        self._canvas.delete(self._canvas_id)
        colors.paddle.trace_vdelete("w", self._paddle_color_trace_observer_name)

import copy
from rong import directions, game_variables, utilities

class Paddle:
    SIZE = utilities.Vector(30, 150)
    __DIAGONAL = SIZE / 2
    __BASE_VELOCITY = utilities.Vector(1000, 1000)
    __ROTATION_RATE = 10
    __BOUNDARY_PADDING = 50
    __BACKGROUND_COLOR = "#aaa"

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

    def __new_points(self, new_position):
        points = [
            new_position + self.__DIAGONAL.inverted,
            new_position + self.__DIAGONAL.inverted_y,
            new_position + self.__DIAGONAL,
            new_position + self.__DIAGONAL.inverted_x
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
                    correction = utilities.displacement_of_collision_of_interval_and_line_to_point_from_reference_from_point(
                        self.position,
                        point,
                        boundary
                    )
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

    def __init__(self, canvas, in_right_half=False):
        self._canvas = canvas
        self._in_right_half = in_right_half

        self._canvas_size = utilities.Vector(
            canvas.winfo_width(),
            canvas.winfo_height()
        )

        x_offset = self.__BOUNDARY_PADDING + self.SIZE.x / 2
        if in_right_half:
            x_offset = (
                self._canvas_size.x
                - self.__BOUNDARY_PADDING
                - self.SIZE.x / 2
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
            fill=self.__BACKGROUND_COLOR
        )

        self.velocity = copy.deepcopy(self.__BASE_VELOCITY)

    def update_position(self, delta_time, pressed_keys):
        delta_speed = self.velocity.magnitude * delta_time
        delta_rotation = self.__ROTATION_RATE * delta_time

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

        velocity = direction * delta_speed

        self.rotation += rotation_increment * delta_rotation
        self.position += velocity
        self.update_position_on_canvas()

    def update_position_on_canvas(self):
        self._canvas.coords(
            self._canvas_id,
            *self.__get_polygon_coordinates()
        )

    def delete(self):
        self._canvas.delete(self._canvas_id)

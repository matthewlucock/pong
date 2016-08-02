import copy
from rong import directions, game_variables, utilities

class Paddle:
    SIZE = utilities.Vector(30, 150)
    __DIAGONAL = SIZE / 2
    __BASE_VELOCITY = utilities.Vector(1000, 1000)
    __ROTATION_RATE = 0.1
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
        points = (
            new_position + self.__DIAGONAL.inverted,
            new_position + self.__DIAGONAL.inverted_y,
            new_position + self.__DIAGONAL,
            new_position + self.__DIAGONAL.inverted_x
        )
        return points

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        new_position = copy.deepcopy(new_position)

        #top_left_vertex = new_position + self.__DIAGONAL.inverted
        #top_right_vertex = new_position + self.__DIAGONAL.inverted_y
        #bottom_right_vertex = new_poisition + self.__DIAGONAL
        #bottom_left_vertex = new_position + self.__DIAGONAL.inverted_x

        points = self.__new_points(new_position)

        if new_position != self.position:
            i = 0
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
                i += 1

        '''
        top_right_vertex = new_position + self.SIZE.x_component
        bottom_left_vertex = new_position + self.SIZE.y_component
        bottom_right_vertex = new_position + self.SIZE

        if new_position.y < 0:
            new_position.y = 0
            self.position = new_position
            return

        if bottom_left_vertex.y > self._canvas_size.y:
            new_position.y -= bottom_left_vertex.y - self._canvas_size.y
            self.position = new_position
            return

        if self._in_right_half:
            if game_variables.free_movement_enabled.get():
                if top_right_vertex.x > self._right_boundary:
                    new_position.x -= (
                        top_right_vertex.x - self._right_boundary
                    )
                    self.position = new_position
                    return

                if new_position.x < self._middle_right_boundary:
                    new_position.x += (
                        self._middle_right_boundary - new_position.x
                    )
                    self.position = new_position
                    return
            elif new_position.x != self._right_boundary:
                return
        elif game_variables.free_movement_enabled.get():
            if new_position.x < self.__BOUNDARY_PADDING:
                new_position.x = self.__BOUNDARY_PADDING
                self.position = new_position
                return

            if new_position.x > self._middle_left_boundary:
                new_position.x = self._middle_left_boundary
                self.position = new_position
                return
        elif new_position.x != self.__BOUNDARY_PADDING:
                return

        self._position = new_position
        self._top_right_vertex = top_right_vertex
        self._bottom_right_vertex = bottom_right_vertex
        self._bottom_left_vertex = bottom_left_vertex
        '''

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

    '''
    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(new_rotation):
        if game_variables.free_movement_enabled.get():
            if utilities.point_is_on_this_side_of_interval
                self._rotation = new_rotation
    '''

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

        '''
        halfway_point = self._canvas_size.x / 2
        self._right_boundary = (
            self._canvas_size.x \
            - self.__BOUNDARY_PADDING \
            - self.SIZE.x
        )
        self._middle_left_boundary = (
            halfway_point - self.__BOUNDARY_PADDING - self.SIZE.x
        )
        self._middle_right_boundary = halfway_point + self.__BOUNDARY_PADDING

        x_offset = self.__BOUNDARY_PADDING

        if in_right_half:
            x_offset = self._right_boundary
            self._keys = self.__RIGHT_HALF_KEYS
        else:
            self._keys = self.__LEFT_HALF_KEYS

        self.position = utilities.Vector(
            x_offset,
            (self._canvas_size.y - self.SIZE.y) / 2
        )
        '''

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

        self._position = utilities.Vector(
            x_offset,
            self._canvas_size.y / 2
        )

        self.position = utilities.Vector(
            x_offset,
            self._canvas_size.y / 2
        )

        self.rotation = 0

        self._canvas_id = canvas.create_polygon(
            *self.__get_polygon_coordinates(),
            fill=self.__BACKGROUND_COLOR
        )

        self.velocity = copy.deepcopy(self.__BASE_VELOCITY)

    def update_position(self, delta_time, pressed_keys):
        delta_speed = self.velocity.magnitude * delta_time

        direction = directions.get_direction_from_keys(
            keys=pressed_keys,
            in_right_half=self._in_right_half
        )
        velocity = direction * delta_speed

        rotation_increment = directions.get_rotation_from_keys(
            keys = pressed_keys,
            in_right_half = self._in_right_half
        )

        #self.rotation += rotation_increment
        self.position += velocity
        self.update_position_on_canvas()

    def update_position_on_canvas(self):
        self._canvas.coords(
            self._canvas_id,
            *self.__get_polygon_coordinates()
        )

    def delete(self):
        self._canvas.delete(self._canvas_id)

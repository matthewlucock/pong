import copy
from rong import directions, game_variables, utilities

class Paddle:
    SIZE = utilities.Vector(30, 150)
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

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        new_position = copy.deepcopy(new_position)

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

        self._intervals = [
            (new_position, top_right_vertex),
            (top_right_vertex, bottom_right_vertex),
            (bottom_left_vertex, bottom_right_vertex),
            (new_position, bottom_left_vertex)
        ]

    def __get_polygon_coordinates(self):
        return (
            self._position.tuple \
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

        self._canvas_id = canvas.create_polygon(
            *self.__get_polygon_coordinates(),
            fill=self.__BACKGROUND_COLOR
        )

        self.velocity = copy.deepcopy(self.__BASE_VELOCITY)

    def rotate(self, rotation):
        pass

    def update_position(self, delta_time, pressed_keys):
        delta_speed = self.velocity.magnitude * delta_time

        direction = directions.get_direction_from_keys(
            keys=pressed_keys,
            in_right_half=self._in_right_half
        )
        velocity = direction * delta_speed

        rotation = directions.get_rotation_from_keys(
            keys = pressed_keys,
            in_right_half = self._in_right_half
        )

        self.rotate(rotation)
        self.position += velocity
        self.update_position_on_canvas()

    def update_position_on_canvas(self):
        self._canvas.coords(
            self._canvas_id,
            *self.__get_polygon_coordinates()
        )

    def delete(self):
        self._canvas.delete(self._canvas_id)

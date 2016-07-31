from rong import utilities

class ZenWall:
    _BACKGROUND_COLOR = "#555"
    _WIDTH = utilities.Vector(x=150)

    def __init__(self, canvas):
        self._canvas = canvas

        top_left_corner = utilities.Vector(
            x=canvas.winfo_width() - self._WIDTH.x
        )

        size = self._WIDTH + utilities.Vector(
            y=canvas.winfo_height()
        )

        self._canvas_id = canvas.create_rectangle(
            *top_left_corner.tuple,
            *(top_left_corner + size).tuple,
            fill=self._BACKGROUND_COLOR
        )
        self._interval = (
            top_left_corner,
            top_left_corner + size.y_component
        )

    def delete(self):
        self._canvas.delete(self._canvas_id)

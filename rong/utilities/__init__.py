import tkinter
from .vector import Vector
from .physics import get_line_collision
from .physics import in_direction
from .physics import point_is_on_line
from .physics import point_is_on_interval
from .physics import point_is_on_this_side_of_interval
from .physics import displacement_of_collision_of_interval_and_line_to_point_from_reference_from_point

def pack_widgets_as_vertical_list(
        widgets,
        margin=20,
        fill_available_width=None,
        anchor=None
):
    if fill_available_width:
        fill_available_width = tkinter.BOTH
    else:
        fill_available_width = None

    for _INDEX, _widget in enumerate(widgets):
        _margin_to_use = margin

        if _INDEX == len(widgets)-1:
            _margin_to_use = 0

        _widget.pack(
            anchor=anchor,
            fill=fill_available_width,
            pady=(0, _margin_to_use)
        )


def toggle_tkinter_boolean_variable(variable):
    if variable.get():
        variable.set(False)
    else:
        variable.set(True)


def get_value_corresponding_to_contrast_level(
        regular_value,
        high_contrast_value
):
    if game_variables.high_contrast_mode_enabled.get():
        return high_contrast_value

    return regular_color


def get_canvas_circle_coordinates(centre, radius):
    radius_vector = Vector(radius, radius)

    return (
        (centre - radius_vector).tuple + (centre+radius_vector).tuple
    )

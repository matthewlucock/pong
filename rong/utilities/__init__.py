import tkinter
import functools
from rong import game_variables
from .vector import Vector
from .physics import get_line_collision
from .physics import in_direction
from .physics import point_is_on_line
from .physics import point_is_on_interval
from .physics import point_is_on_this_side_of_interval
from .physics import midpoint
from .physics import vector_to_line

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

    return regular_value


def set_tkinter_variable_corresponding_to_tkinter_boolean_variable(
        variable_to_check,
        variable_to_set,
        true_value,
        false_value
):
    if variable_to_check.get():
        variable_to_set.set(true_value)
    else:
        variable_to_set.set(false_value)


def link_tkinter_variable_to_tkinter_boolean_variable(
        variable_to_trace,
        variable_to_modify,
        true_value,
        false_value
):
    set_variable = functools.partial(
        set_tkinter_variable_corresponding_to_tkinter_boolean_variable,
        variable_to_check=variable_to_trace,
        variable_to_set=variable_to_modify,
        true_value=true_value,
        false_value=false_value
    )

    set_variable()

    variable_to_trace.trace("w", lambda *args: set_variable())


def get_canvas_circle_coordinates(centre, radius):
    radius_vector = Vector(radius, radius)

    return (
        (centre - radius_vector).tuple + (centre+radius_vector).tuple
    )

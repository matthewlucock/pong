import tkinter
import functools
from . import game_variables, utilities

_link_tkinter_variable_to_high_contrast_mode_enabled = functools.partial(
    utilities.link_tkinter_variable_to_tkinter_boolean_variable,
    variable_to_trace=game_variables.high_contrast_mode_enabled
)

screen_background = tkinter.StringVar()
title = tkinter.StringVar()
settings_container_background = tkinter.StringVar()

button_background = tkinter.StringVar()
button_mouseover_background = tkinter.StringVar()
button_text = tkinter.StringVar()

checkbox_text = tkinter.StringVar()
checkmark_container_background = tkinter.StringVar()

pause_button_background = tkinter.StringVar()
ball = tkinter.StringVar()
paddle = tkinter.StringVar()

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=screen_background,
    true_value="black",
    false_value="#2c3e50"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=title,
    true_value="white",
    false_value="white"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=settings_container_background,
    true_value="white",
    false_value="#16a085"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=button_background,
    true_value="white",
    false_value="#2980b9"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=button_mouseover_background,
    true_value="#888",
    false_value="#3498db"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=button_text,
    true_value="black",
    false_value="white"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=checkbox_text,
    true_value="black",
    false_value="white"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=checkmark_container_background,
    true_value="gray",
    false_value="#2ecc71"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=checkmark_container_background,
    true_value="gray",
    false_value="#2ecc71"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=pause_button_background,
    true_value="gray",
    false_value="#2980b9"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=ball,
    true_value="black",
    false_value="#d35400"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=paddle,
    true_value="black",
    false_value="#96281b"
)

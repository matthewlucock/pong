import tkinter
import functools
from . import game_variables, utilities

_link_tkinter_variable_to_high_contrast_mode_enabled = functools.partial(
    utilities.link_tkinter_variable_to_tkinter_boolean_variable,
    variable_to_trace=game_variables.high_contrast_mode_enabled
)

screen_background = tkinter.StringVar()
title = tkinter.StringVar()

button_background = tkinter.StringVar()
button_mouseover_background = tkinter.StringVar()
button_text = tkinter.StringVar()

checkbox_text = tkinter.StringVar()

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=screen_background,
    true_value="black",
    false_value="white"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=title,
    true_value="white",
    false_value="black"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=button_background,
    true_value="#aaa",
    false_value="#aaa"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=button_mouseover_background,
    true_value="#888",
    false_value="#888"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=button_text,
    true_value="black",
    false_value="black"
)

_link_tkinter_variable_to_high_contrast_mode_enabled(
    variable_to_modify=checkbox_text,
    true_value="white",
    false_value="black"
)

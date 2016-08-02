import tkinter
from rong import custom_widgets, colors, fonts, game_variables, game_modes, \
    event_names, utilities
from rong.screen_manager import screen_manager


multiplayer_screen = tkinter.Frame()

_title = tkinter.Label(
    master=multiplayer_screen,
    text="Multiplayer",
    font=fonts.side_screen_title_font,
    anchor=tkinter.CENTER
)
_title.pack(pady=(30, 0))

_settings_container = tkinter.Frame(
    master=multiplayer_screen,
    **custom_widgets.miscellaneous_widget_parameters.SETTINGS_CONTAINER
)
_settings_container.pack(expand=True)

_power_ups_checkbox = custom_widgets.StyledCheckbox(
    master=_settings_container,
    variable=game_variables.power_ups_enabled,
    text="Power-ups"
)

_free_movement_checkbox = custom_widgets.StyledCheckbox(
    master=_settings_container,
    variable=game_variables.free_movement_enabled,
    text="Free movement"
)

utilities.pack_widgets_as_vertical_list(
    widgets=[_power_ups_checkbox, _free_movement_checkbox],
    anchor=tkinter.W,
    margin=10
)

_buttons_container = tkinter.Frame(master=multiplayer_screen)
_buttons_container.pack(pady=(0, 50))

_play_button = custom_widgets.PlayButton(
    master=_buttons_container,
    game_mode=game_modes.MULTIPLAYER
)
_back_button = custom_widgets.BackButton(master=_buttons_container)

utilities.pack_widgets_as_vertical_list(
    widgets=[_play_button, _back_button],
    fill_available_width=True
)

_widgets_to_set_background_of = [
    multiplayer_screen,
    _title,
    _buttons_container
]


def _screen_background_color_trace_callback(*args):
    for _widget in _widgets_to_set_background_of:
        _widget.config(
            background=colors.screen_background.get()
        )


def _title_color_trace_callback(*args):
    _title.config(foreground=colors.title.get())


_screen_background_color_trace_callback()
_title_color_trace_callback()
colors.screen_background.trace("w", _screen_background_color_trace_callback)
colors.title.trace("w", _title_color_trace_callback)

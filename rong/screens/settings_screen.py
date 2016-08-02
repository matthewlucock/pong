import tkinter
from rong import custom_widgets, colors, fonts, game_variables, event_names, \
    utilities
from rong.screen_manager import screen_manager


settings_screen = tkinter.Frame()

_title = tkinter.Label(
    master=settings_screen,
    text="Settings",
    font=fonts.side_screen_title_font
)
_title.pack(pady=(30, 0))

_settings_container = tkinter.Frame(
    master=settings_screen,
    **custom_widgets.miscellaneous_widget_parameters.SETTINGS_CONTAINER
)
_settings_container.pack(expand=True)

_high_contrast_checkbox = custom_widgets.StyledCheckbox(
    master=_settings_container,
    variable=game_variables.high_contrast_mode_enabled,
    text="High contrast"
)
_high_contrast_checkbox.pack(anchor=tkinter.W)

_back_button = custom_widgets.BackButton(master=settings_screen)
_back_button.pack(pady=(0, 50))

_widgets_to_set_background_of = [
    settings_screen,
    _title
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

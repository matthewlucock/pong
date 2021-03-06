import tkinter
from rong import custom_widgets, colors, fonts, event_names, utilities
from rong.screen_manager import screen_manager

from .versus_ai_screen import versus_ai_screen
from .multiplayer_screen import multiplayer_screen
from .zen_screen import zen_screen
from .settings_screen import settings_screen
from . import help_screen


main_screen = tkinter.Frame()

_title = tkinter.Label(
    master=main_screen,
    text="Rong",
    font=fonts.main_screen_title_font
)
_title.pack()

_menus_container = tkinter.Frame(master=main_screen)
_menus_container.pack(expand=True)

_modes_menu = tkinter.Frame(master=_menus_container)
_modes_menu.pack(side=tkinter.LEFT, padx=(0, 300))

_miscellaneous_menu = tkinter.Frame(master=_menus_container)
_miscellaneous_menu.pack(expand=True)

_menus_data = [
    {
        "master": _modes_menu,
        "buttons": [
            {"text": "Versus AI", "screen": versus_ai_screen},
            {"text": "Multiplayer", "screen": multiplayer_screen},
            {"text": "Zen", "screen": zen_screen}
        ]
    },
    {
        "master": _miscellaneous_menu,
        "buttons": [
            {"text": "Settings", "screen": settings_screen},
            {
                "text": "Help",
                "screen": help_screen.help_screen,
                "back_button": help_screen.back_button
            }
        ]
    }
]


def _make_function_that_changes_screen(button_data):
    def change_screen(*args):
        back_button = button_data.get("back_button")

        if back_button:
            back_button.source_screen = main_screen

        screen_manager.change_screen(button_data["screen"])

    return change_screen


for _individual_menu_data in _menus_data:
    _menu_buttons = []

    for _button_data in _individual_menu_data["buttons"]:
        _button = custom_widgets.StyledButton(
            master=_individual_menu_data["master"],
            text=_button_data["text"]
        )
        _button.bind(
            event_names.LEFT_CLICK,
            _make_function_that_changes_screen(_button_data)
        )
        _menu_buttons.append(_button)

    utilities.pack_widgets_as_vertical_list(
        widgets=_menu_buttons,
        fill_available_width=True
    )

_widgets_to_update_background_of = [
    main_screen,
    _title,
    _menus_container,
    _modes_menu,
    _miscellaneous_menu
]


def _screen_background_color_trace_callback(*args):
    for _widget in _widgets_to_update_background_of:
        _widget.config(
            background=colors.screen_background.get()
        )


def _title_color_trace_callback(*args):
    _title.config(foreground=colors.title.get())


_screen_background_color_trace_callback()
_title_color_trace_callback()
colors.screen_background.trace("w", _screen_background_color_trace_callback)
colors.title.trace("w", _title_color_trace_callback)

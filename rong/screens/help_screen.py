import tkinter
import functools
from rong import custom_widgets, fonts, colors, event_names, utilities
from rong.screen_manager import screen_manager
from . import help_file_screen

help_screen = tkinter.Frame()

_title = tkinter.Label(
    master=help_screen,
    text="Help",
    font=fonts.side_screen_title_font
)
_title.pack()

_menus_container = tkinter.Frame(master=help_screen)
_menus_container.pack(expand=True)

_menus_help_menu = tkinter.Frame(master=_menus_container)
_menus_help_menu.pack(side=tkinter.LEFT, padx=(0, 300))

_gameplay_help_menu = tkinter.Frame(master=_menus_container)
_gameplay_help_menu.pack(expand=True)

back_button = custom_widgets.BackButton(master=help_screen)
back_button.pack(pady=(0, 20))

_HELP_FILES_PATH_TEMPLATE = "rong/help/{}.txt"

_MENUS_HELP_FILES_LIST = [
    {"title": "Introduction", "file_name": "01 Introduction"},
    {"title": "Main menu", "file_name": "02 Main Menu"},
    {"title": "Game menus", "file_name": "03 Game Menus"},
    {"title": "Settings menu", "file_name": "04 Settings Menu"},
    {"title": "Help menu", "file_name": "05 Help Menu"}
]

_GAMEPLAY_HELP_FILES_LIST = [
    {"title": "Controls", "file_name": "06 Controls"},
    {"title": "Versus AI", "file_name": "07 Versus AI"},
    {"title": "Multiplayer", "file_name": "08 Multiplayer"},
    {"title": "Zen mode", "file_name": "09 Zen Mode"},
    {"title": "Power-ups", "file_name": "10 Power Ups"},
    {"title": "Free movement", "file_name": "11 Free Movement"}
]

_menus_data = [
    {"master": _menus_help_menu, "files": _MENUS_HELP_FILES_LIST},
    {"master": _gameplay_help_menu, "files": _GAMEPLAY_HELP_FILES_LIST}
]

_help_files_text = {}

for _help_screen_data in (_MENUS_HELP_FILES_LIST + _GAMEPLAY_HELP_FILES_LIST):
    _file_name = _help_screen_data["file_name"]

    with open(_HELP_FILES_PATH_TEMPLATE.format(_file_name)) as _file:
        _help_files_text[_file_name] = _file.read()


def _make_change_to_help_file_screen_function(title, text):
    def change_to_help_file_screen(*args):
        help_file_screen.init(title=title, text=text)
        screen_manager.change_screen(help_file_screen.help_file_screen)
        pass

    return change_to_help_file_screen


for _individual_menu_data in _menus_data:
    _menu_buttons = []

    for _button_data in _individual_menu_data["files"]:
        _button = custom_widgets.StyledButton(
            master=_individual_menu_data["master"],
            text=_button_data["title"]
        )
        _button.config(font=fonts.help_button_font)
        _button.bind(
            event_names.LEFT_CLICK,
            _make_change_to_help_file_screen_function(
                title=_button_data["title"],
                text=_help_files_text[_button_data["file_name"]]
            )
        )
        _menu_buttons.append(_button)

    utilities.pack_widgets_as_vertical_list(
        widgets=_menu_buttons,
        fill_available_width=True
    )

_widgets_to_update_background_of = [
    help_screen,
    _title,
    _menus_container,
    _menus_help_menu,
    _gameplay_help_menu
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

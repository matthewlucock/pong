import tkinter
from rong import custom_widgets, images, game_variables, event_names, fonts, \
    utilities
from rong.screen_manager import screen_manager
from rong.custom_widgets import StyledButton, miscellaneous_widget_parameters
from rong.game import Game
from .settings_screen import settings_screen


_SCREEN_BACKGROUND_COLOR = "#aaa"
_PAUSE_BUTTON_COLOR = "#ccc"
_CANVAS_BACKGROUND_COLOR = "white"
_DIVIDER_COLOR = "black"
_GUTTER_HEIGHT = 50
_BORDER_WIDTH = 10

current_game = None

def _make_divider():
    return tkinter.Frame(
        master=game_screen,
        background=_DIVIDER_COLOR,
        height=_BORDER_WIDTH
    )

game_screen = tkinter.Frame(background=_SCREEN_BACKGROUND_COLOR)

_space_above_canvas = tkinter.Frame(
    master=game_screen,
    background=_SCREEN_BACKGROUND_COLOR
)
_space_above_canvas.pack(fill=tkinter.X)

_pause_button_container = tkinter.Frame(
    master=_space_above_canvas,
    background=_PAUSE_BUTTON_COLOR
)
_pause_button_container.pack(side=tkinter.RIGHT)

_pause_button_container_divider = tkinter.Frame(
    master=_pause_button_container,
    background=_DIVIDER_COLOR,
    width=_BORDER_WIDTH,
    height=_GUTTER_HEIGHT
)
_pause_button_container_divider.pack(side=tkinter.LEFT)

_pause_glyph = tkinter.Label(
    master=_pause_button_container,
    image=images.TKINTER_USEABLE_PAUSE_GLYPH,
    background=_PAUSE_BUTTON_COLOR,
    borderwidth=0
)
_pause_glyph.pack(pady=10, padx=10)

_make_divider().pack(fill=tkinter.BOTH)

canvas = tkinter.Canvas(
    master=game_screen,
    background=_CANVAS_BACKGROUND_COLOR,
    highlightthickness=0
)
canvas.pack(fill=tkinter.BOTH, expand=True)

_make_divider().pack(pady=(0, _GUTTER_HEIGHT), fill=tkinter.BOTH)


def _pause_button_callback(*args):
    Game.current_game.pause()
    _pause_menu_container.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

for _widget in [_pause_button_container, _pause_glyph]:
    _widget.bind(event_names.LEFT_CLICK, _pause_button_callback)

_PAUSE_SCREEN_BACKGROUND_COLOR = "#333"

_pause_menu_container = tkinter.Frame(
    master=game_screen,
    background=_PAUSE_SCREEN_BACKGROUND_COLOR,
    **miscellaneous_widget_parameters.SETTINGS_CONTAINER
)

_pause_menu_buttons = tkinter.Frame(
    master=_pause_menu_container,
    background=_PAUSE_SCREEN_BACKGROUND_COLOR
)
_pause_menu_buttons.pack()

_continue_button = custom_widgets.StyledButton(
    master=_pause_menu_buttons,
    text="Continue"
)
_settings_button = custom_widgets.StyledButton(
    master=_pause_menu_buttons,
    text="Settings"
)
_help_button = custom_widgets.StyledButton(
    master=_pause_menu_buttons,
    text="Help"
)
_quit_button = custom_widgets.StyledButton(
    master=_pause_menu_buttons,
    text="Quit"
)

utilities.pack_widgets_as_vertical_list(
    widgets=[_continue_button, _settings_button, _help_button, _quit_button],
    fill_available_width=True
)

_quit_confirmation_container = tkinter.Frame(
    master=_pause_menu_container,
    background=_PAUSE_SCREEN_BACKGROUND_COLOR
)

_quit_confirmation_text = tkinter.Label(
    master=_quit_confirmation_container,
    text="Are you sure you want to quit?",
    font="Arial 50",
    **custom_widgets.miscellaneous_widget_parameters.SETTINGS_CONTAINER
)
_quit_confirmation_text.pack(expand=True)

_quit_confirmation_buttons = tkinter.Frame(
    master=_quit_confirmation_container,
    background=_PAUSE_SCREEN_BACKGROUND_COLOR
)
_quit_confirmation_buttons.pack(pady=(100, 0))

_quit_cancel_button = custom_widgets.StyledButton(
    master=_quit_confirmation_buttons,
    text="No"
)
_quit_confirm_button = custom_widgets.StyledButton(
    master=_quit_confirmation_buttons,
    text="Yes"
)

_quit_cancel_button.pack(side=tkinter.LEFT, padx=(0, 100))
_quit_confirm_button.pack()


def _continue_button_callback(*args):
    _pause_menu_container.place_forget()
    Game.current_game.resume()


def _settings_button_callback(*args):
    screen_manager.change_screen(settings_screen)


def _quit_button_callback(*args):
    _pause_menu_buttons.pack_forget()
    _quit_confirmation_container.pack(expand=True, anchor=tkinter.CENTER)


def _quit_cancel_button_callback(*args):
    _quit_confirmation_container.pack_forget()
    _pause_menu_buttons.pack()


def _quit_confirm_button_callback(*args):
    Game.current_game.destroy()
    _quit_confirmation_container.pack_forget()
    _pause_menu_buttons.pack()
    _pause_menu_container.place_forget()
    screen_manager.change_screen(screen_manager.main_screen)


_continue_button.bind(event_names.LEFT_CLICK, _continue_button_callback)
_settings_button.bind(event_names.LEFT_CLICK, _settings_button_callback)
_quit_button.bind(event_names.LEFT_CLICK, _quit_button_callback)
_quit_cancel_button.bind(event_names.LEFT_CLICK, _quit_cancel_button_callback)
_quit_confirm_button.bind(
    event_names.LEFT_CLICK,
    _quit_confirm_button_callback
)

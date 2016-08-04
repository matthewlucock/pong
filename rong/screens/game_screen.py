import tkinter
from rong import custom_widgets, colors, images, game_variables, fonts, \
    event_names, fonts, utilities, game_modes
from rong.screen_manager import screen_manager
from rong.custom_widgets import StyledButton, miscellaneous_widget_parameters
from rong.game import Game
from rong.game.ball import Ball
from .settings_screen import settings_screen
from . import help_screen, game_over_screen


_GUTTER_HEIGHT = 50
_BORDER_WIDTH = 10
_SCORE_TEMPLATE = "{player_one_score} — {player_two_score}"

current_game = None

game_screen = tkinter.Frame()

_space_above_canvas = tkinter.Frame(master=game_screen)
_space_above_canvas.pack(fill=tkinter.X)

_score = tkinter.Label(
    master=_space_above_canvas,
    font=fonts.button_font,
    foreground="white"
)
_score.pack(expand=True, side=tkinter.LEFT)
Game.score_label = _score

_pause_button_container = tkinter.Frame(master=_space_above_canvas)
_pause_button_container.pack(side=tkinter.RIGHT)

_pause_glyph = tkinter.Label(
    master=_pause_button_container,
    image=images.TKINTER_USEABLE_PAUSE_GLYPH,
    borderwidth=0
)
_pause_glyph.pack(pady=10, padx=10)

canvas = tkinter.Canvas(master=game_screen, highlightthickness=0)
canvas.pack(fill=tkinter.BOTH, expand=True, pady=(0, _GUTTER_HEIGHT))
Game.canvas = canvas

def _pause_button_callback(*args):
    Game.current_game.pause()
    _pause_menu_container.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

for _widget in [_pause_button_container, _pause_glyph]:
    _widget.bind(event_names.LEFT_CLICK, _pause_button_callback)

Game.open_pause_menu = _pause_button_callback

_pause_menu_container = tkinter.Frame(
    master=game_screen,
    **miscellaneous_widget_parameters.SETTINGS_CONTAINER
)

Game.close_pause_menu = _pause_menu_container.place_forget

_pause_menu_buttons = tkinter.Frame(master=_pause_menu_container)
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

_quit_confirmation_container = tkinter.Frame(master=_pause_menu_container)

_quit_confirmation_text = tkinter.Label(
    master=_quit_confirmation_container,
    text="Are you sure you want to quit?",
    font="Arial 50",
    foreground="white",
    **custom_widgets.miscellaneous_widget_parameters.SETTINGS_CONTAINER
)
_quit_confirmation_text.pack(expand=True)

_quit_confirmation_buttons = tkinter.Frame(master=_quit_confirmation_container)
_quit_confirmation_buttons.pack()

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

_widgets_to_have_screen_background = [
    game_screen,
    _pause_menu_container,
    _pause_menu_buttons,
    _quit_confirmation_container,
    _quit_confirmation_text,
    _quit_confirmation_buttons,
    _space_above_canvas,
    _score
]

_widgets_to_have_button_background = [
    _pause_button_container,
    _pause_glyph
]

def _screen_background_color_trace_callback(*args):
    for _widget in _widgets_to_have_screen_background:
        _widget.config(background=colors.screen_background.get())


def _pause_button_background_color_trace_callback(*args):
    for _widget in _widgets_to_have_button_background:
        _widget.config(background=colors.pause_button_background.get())

def _set_pause_glpyh():
    pause_glpyh = utilities.get_value_corresponding_to_contrast_level(
        regular_value=images.TKINTER_USEABLE_PAUSE_GLYPH,
        high_contrast_value=images.TKINTER_USEABLE_BLACK_PAUSE_GLYPH
    )
    _pause_glyph.config(image=pause_glpyh)

_screen_background_color_trace_callback()
_pause_button_background_color_trace_callback()
_set_pause_glpyh()
colors.screen_background.trace("w", _screen_background_color_trace_callback)
colors.pause_button_background.trace(
    "w",
    _pause_button_background_color_trace_callback
)
game_variables.high_contrast_mode_enabled.trace(
    "w",
    lambda *args: _set_pause_glpyh()
)


def destroy():
    Game.current_game.destroy()
    _quit_confirmation_container.pack_forget()
    _pause_menu_buttons.pack()
    _pause_menu_container.place_forget()

_player_one_score_observer_name = tkinter.StringVar()
_player_two_score_observer_name = tkinter.StringVar()

def set_score():
    player_one_score = game_variables.player_one_score.get()
    player_two_score = game_variables.player_two_score.get()
    score_limit = game_variables.score_limit.get()

    if (
            game_variables.game_mode.get() != game_modes.ZEN and (
                player_one_score >= score_limit
                or player_two_score >= score_limit
            )
    ):
        destroy()
        game_over_screen.init()
        screen_manager.change_screen(game_over_screen.game_over_screen)
        return

    score_text = _SCORE_TEMPLATE.format(
        player_one_score=player_one_score,
        player_two_score=player_two_score
    )
    _score.config(text=score_text)

Ball.set_score_label = set_score


def _continue_button_callback(*args):
    _pause_menu_container.place_forget()
    Game.current_game.resume()


def _settings_button_callback(*args):
    screen_manager.change_screen(settings_screen)


def _help_button_callback(*args):
    help_screen.back_button.source_screen = game_screen
    screen_manager.change_screen(help_screen.help_screen)


def _quit_button_callback(*args):
    _pause_menu_buttons.pack_forget()
    _quit_confirmation_container.pack(expand=True, anchor=tkinter.CENTER)


def _quit_cancel_button_callback(*args):
    _quit_confirmation_container.pack_forget()
    _pause_menu_buttons.pack()


def _quit_confirm_button_callback(*args):
    destroy()
    screen_manager.change_screen(screen_manager.main_screen)


_continue_button.bind(event_names.LEFT_CLICK, _continue_button_callback)
_settings_button.bind(event_names.LEFT_CLICK, _settings_button_callback)
_help_button.bind(event_names.LEFT_CLICK, _help_button_callback)
_quit_button.bind(event_names.LEFT_CLICK, _quit_button_callback)
_quit_cancel_button.bind(event_names.LEFT_CLICK, _quit_cancel_button_callback)
_quit_confirm_button.bind(
    event_names.LEFT_CLICK,
    _quit_confirm_button_callback
)

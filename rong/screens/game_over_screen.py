import tkinter
from rong import game_variables, custom_widgets, fonts, event_names, \
    game_modes, colors, utilities
from rong.screen_manager import screen_manager

_SCORE_TEMPLATE = "{player_one_score} — {player_two_score}"

game_over_screen = tkinter.Frame()

_content_container = tkinter.Frame(master=game_over_screen)
_content_container.pack(expand=True)

_heading = tkinter.Label(
    master=_content_container,
    font=fonts.side_screen_title_font,
    foreground="white"
)
_heading.pack(pady=(0, 50))

_score = tkinter.Label(
    master=_content_container,
    font=fonts.button_font,
    foreground="white"
)
_score.pack(pady=(0, 50))

_buttons = tkinter.Frame(master=_content_container)
_buttons.pack()

_restart_button = custom_widgets.PlayButton(master=_buttons)
_restart_button.config(text="Restart")

_quit_button = custom_widgets.StyledButton(master=_buttons, text="Quit")

utilities.pack_widgets_as_vertical_list(
    widgets=[_restart_button, _quit_button],
    fill_available_width=True
)

def _quit_button_callback(*args):
    screen_manager.change_screen(screen_manager.main_screen)


_quit_button.bind(event_names.LEFT_CLICK, _quit_button_callback)


def init():
    _restart_button.game_mode = game_variables.game_mode.get()

    player_one_score = game_variables.player_one_score.get()
    player_two_score = game_variables.player_two_score.get()

    score_text = _SCORE_TEMPLATE.format(
        player_one_score=player_one_score,
        player_two_score=player_two_score
    )
    _score.config(text=score_text)

    name_of_player_that_won = None

    if player_one_score >= game_variables.score_limit.get():
        name_of_player_that_won = "Player 1"
    elif game_variables.game_mode.get() == game_modes.MULTIPLAYER:
        name_of_player_that_won = "Player 2"
    else:
        name_of_player_that_won = "The AI"

    _heading.config(text=name_of_player_that_won + " has won!")

_widgets_to_have_screen_background = [
    game_over_screen,
    _content_container,
    _heading,
    _score,
    _buttons
]

def _screen_background_color_trace_callback(*args):
    for _widget in _widgets_to_have_screen_background:
        _widget.config(
            background=colors.screen_background.get()
        )

_screen_background_color_trace_callback()
colors.screen_background.trace("w", _screen_background_color_trace_callback)

import tkinter
from rong import custom_widgets, fonts, game_variables, game_modes, \
    event_names, utilities
from rong.screen_manager import screen_manager


campaign_screen = tkinter.Frame()

_title = tkinter.Label(
    master=campaign_screen,
    text="Campaign",
    font=fonts.side_screen_title_font
)
_title.pack(pady=(30, 0))

_settings_container = tkinter.Frame(
    master=campaign_screen,
    **custom_widgets.miscellaneous_widget_parameters.SETTINGS_CONTAINER
)
_settings_container.pack(expand=True)

_level_selector = custom_widgets.IntegerSelector(
    master=_settings_container,
    variable=game_variables.selected_campaign_level,
    minimum_value=1,
    maximum_value=10,
    text="Level select"
)
_level_selector.pack(expand=True)

_buttons_container = tkinter.Frame(master=campaign_screen)
_buttons_container.pack(pady=(0, 50))

_play_button = custom_widgets.PlayButton(
    master=_buttons_container,
    game_mode=game_modes.CAMPAIGN
)
_back_button = custom_widgets.BackButton(master=_buttons_container)

utilities.pack_widgets_as_vertical_list(
    widgets=[_play_button, _back_button],
    fill_available_width=True
)

import tkinter
from rong import custom_widgets, fonts, colors, event_names, utilities

help_file_screen = tkinter.Frame()

_title = tkinter.Label(
    master=help_file_screen,
    text="Help",
    font=fonts.side_screen_title_font
)
_title.pack()

_help_file_text = tkinter.Message(
    master=help_file_screen,
    width=600,
    foreground="white",
    justify=tkinter.CENTER
)
_help_file_text.pack(expand=True)

_back_button = custom_widgets.BackButton(master=help_file_screen)
_back_button.pack(pady=(0, 20))


def init(title, text, font_size=None):
    if font_size is None:
        font_size = 15

    _title.config(text=title)
    _help_file_text.config(text=text, font="Arial " + str(font_size))

_widgets_to_update_background_of = [
    help_file_screen,
    _title,
    _help_file_text
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

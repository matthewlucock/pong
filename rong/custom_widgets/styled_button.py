import tkinter
from rong import colors, fonts, event_names, utilities


class StyledButton(tkinter.Label):
    def __set_standard_background(self):
        self.config(background=colors.button_background.get())

    def __set_mousover_background(self):
        self.config(background=colors.button_mouseover_background.get())

    def __set_text_color(self):
        self.config(foreground=colors.button_text.get())

    def __init__(self, master, text):
        super().__init__(
            master=master,
            text=text,
            font=fonts.button_font,
            borderwidth=10,
            relief=tkinter.SOLID,
            padx=10,
            pady=5
        )

        self.__set_standard_background()
        self.__set_text_color()

        colors.button_background.trace(
            "w",
            lambda *args: self.__set_standard_background()
        )

        colors.button_text.trace("w", lambda *args: self.__set_text_color())

        event_handlers = [
            (
                event_names.MOUSEOVER,
                lambda *args: self.__set_mousover_background()
            ),
            (
                event_names.MOUSEOUT,
                lambda *args: self.__set_standard_background()
            )
        ]

        for _args in event_handlers:
            self.bind(*_args)

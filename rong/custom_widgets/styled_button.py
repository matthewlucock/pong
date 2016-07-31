import tkinter
from rong import fonts, event_names


class StyledButton(tkinter.Label):
    __BACKGROUND_COLOR = "#aaa"
    __MOUSEOVER_BACKGROUND_COLOR = "#777"

    def __mouseover_callback(self, *args):
        self.config(background=self.__MOUSEOVER_BACKGROUND_COLOR)

    def __mouseout_callback(self, *args):
        self.config(background=self.__BACKGROUND_COLOR)

    def __init__(self, master, text):
        super().__init__(
            master=master,
            text=text,
            font=fonts.button_font,
            background=self.__BACKGROUND_COLOR,
            borderwidth=10,
            relief=tkinter.SOLID,
            padx=10,
            pady=5
        )

        event_handlers = [
            (event_names.MOUSEOVER, self.__mouseover_callback),
            (event_names.MOUSEOUT, self.__mouseout_callback)
        ]

        for _args in event_handlers:
            self.bind(*_args)

import tkinter
import functools
from rong import images, colors, fonts, event_names, game_variables, utilities


class StyledCheckbox(tkinter.Frame):
    __CHECKBOX_SIZE = 40
    __CHECKMARK_CONTAINER_BORDER_WIDTH = 5
    __SPACE_BETWEEN_CHECKMARK_AND_LABEL = 20

    __get_checkmark_image = functools.partial(
        utilities.get_value_corresponding_to_contrast_level,
        regular_value=images.TKINTER_USABLE_INVERTED_CHECKMARK,
        high_contrast_value=images.TKINTER_USABLE_CHECKMARK
    )

    def __set_checkmark_state(self):
        if self._variable.get():
            self._checkmark.config(image=self.__get_checkmark_image())
        else:
            self._checkmark.pack_forget()

    def __set_text_color(self):
        self._text.config(foreground=colors.checkbox_text.get())

    def __init__(self, master, variable, text):
        super().__init__(master)

        self._variable = variable

        self._checkmark_container = tkinter.Frame(
            self,
            height=self.__CHECKBOX_SIZE,
            width=self.__CHECKBOX_SIZE,
            borderwidth=5,
            relief=tkinter.SOLID,
        )
        self._checkmark_container.pack(
            side=tkinter.LEFT,
            padx=(0, self.__SPACE_BETWEEN_CHECKMARK_AND_LABEL)
        )

        self._checkmark = tkinter.Label(
            self._checkmark_container,
            image=images.TKINTER_USABLE_CHECKMARK,
            borderwidth=0
        )

        self.__set_checkmark_state()

        variable.trace("w", lambda *args: self.__set_checkmark_state())
        game_variables.high_contrast_mode_enabled.trace(
            "w",
            lambda *args: self.__set_checkmark_state()
        )

        self._text = tkinter.Label(self, text=text, font=fonts.checkbox_font)
        self._text.pack()

        self.__set_text_color()

        colors.checkbox_text.trace("w", lambda *args: self.__set_text_color())

        click_handler_arguments = (
            event_names.LEFT_CLICK,
            lambda *args: utilities.toggle_tkinter_boolean_variable(variable)
        )

        widgets_to_bind_click_handler_to = [
            self,
            self._checkmark,
            self._checkmark_container,
            self._text
        ]

        for _widget in widgets_to_bind_click_handler_to:
            _widget.bind(*click_handler_arguments)

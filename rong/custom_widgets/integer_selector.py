import tkinter
from rong import fonts, event_names, images


class IntegerSelector(tkinter.Frame):
    __VALUE_LABEL_BORDER_WIDTH = 5
    __SPACE_BETWEEN_MODIFIER_BUTTONS_AND_VALUE_LABEL = 40

    def __set_variable(self, new_value):
        if self._minimum_value <= new_value <= self._maximum_value:
            self._variable.set(new_value)

    def __variable_trace_callback(self, *args):
        self._value_label.config(text=self._variable.get())

    def __decrement_button_callback(self, *args):
        self.__set_variable(self._variable.get() - 1)

    def __increment_button_callback(self, *args):
        self.__set_variable(self._variable.get() + 1)

    def __init__(self, master, variable, minimum_value, maximum_value, text):
        if not (minimum_value <= variable.get() <= maximum_value):
            raise Exception

        super().__init__(master)

        self._variable = variable
        self._minimum_value = minimum_value
        self._maximum_value = maximum_value

        variable.trace("w", self.__variable_trace_callback)

        heading = tkinter.Label(self, text=text, font=fonts.button_font)

        self._value_label = tkinter.Label(
            self,
            text=self._variable.get(),
            borderwidth=self.__VALUE_LABEL_BORDER_WIDTH,
            relief=tkinter.SOLID,
            width=3,
            padx=10,
            pady=5,
            font=fonts.button_font
        )

        decrement_button = tkinter.Label(
            self,
            image=images.TKINTER_USABLE_LEFT_POINTING_ARROW
        )

        increment_button = tkinter.Label(
            self,
            image=images.TKINTER_USABLE_RIGHT_POINTING_ARROW
        )

        heading.pack(pady=(0, 10))

        decrement_button.pack(
            expand=True,
            side=tkinter.LEFT,
            padx=(0, self.__SPACE_BETWEEN_MODIFIER_BUTTONS_AND_VALUE_LABEL)
        )

        self._value_label.pack(side=tkinter.LEFT)

        increment_button.pack(
            expand=True,
            padx=(self.__SPACE_BETWEEN_MODIFIER_BUTTONS_AND_VALUE_LABEL, 0)
        )

        decrement_button.bind(
            event_names.LEFT_CLICK,
            self.__decrement_button_callback
        )

        increment_button.bind(
            event_names.LEFT_CLICK,
            self.__increment_button_callback
        )

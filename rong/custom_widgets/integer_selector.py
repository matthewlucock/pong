import tkinter
from rong import fonts, event_names, colors, images, game_variables


class IntegerSelector(tkinter.Frame):
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

    def __set_value_background_color(self):
        self._value_label.config(
            background=colors.checkmark_container_background.get()
        )

    def __set_text_color(self):
        text_color = colors.button_text.get()

        widgets_to_set_text_color_of = [self._heading, self._value_label]

        for _widget in widgets_to_set_text_color_of:
            _widget.config(foreground=text_color)

    def __set_button_images(self):
        decrement_button_image = None
        increment_button_image = None

        if game_variables.high_contrast_mode_enabled.get():
            decrement_button_image = (
                images.TKINTER_USABLE_LEFT_POINTING_BLACK_ARROW
            )
            increment_button_image = (
                images.TKINTER_USABLE_RIGHT_POINTING_BLACK_ARROW
            )
        else:
            decrement_button_image = images.TKINTER_USABLE_LEFT_POINTING_ARROW
            increment_button_image = images.TKINTER_USABLE_RIGHT_POINTING_ARROW

        self._decrement_button.config(image=decrement_button_image)
        self._increment_button.config(image=increment_button_image)

    def __init__(self, master, variable, minimum_value, maximum_value, text):
        if not (minimum_value <= variable.get() <= maximum_value):
            raise Exception

        super().__init__(master)

        self._variable = variable
        self._minimum_value = minimum_value
        self._maximum_value = maximum_value

        variable.trace("w", self.__variable_trace_callback)

        self._heading = tkinter.Label(self, text=text, font=fonts.button_font)

        self._value_label = tkinter.Label(
            self,
            text=self._variable.get(),
            width=3,
            padx=10,
            pady=5,
            font=fonts.button_font
        )

        self._decrement_button = tkinter.Label(master=self)
        self._increment_button = tkinter.Label(master=self)

        self.__set_button_images()
        game_variables.high_contrast_mode_enabled.trace(
            "w",
            lambda *args: self.__set_button_images()
        )

        self._heading.pack(pady=(0, 10))

        self._decrement_button.pack(
            expand=True,
            side=tkinter.LEFT,
            padx=(0, self.__SPACE_BETWEEN_MODIFIER_BUTTONS_AND_VALUE_LABEL)
        )

        self._value_label.pack(side=tkinter.LEFT)

        self._increment_button.pack(
            expand=True,
            padx=(self.__SPACE_BETWEEN_MODIFIER_BUTTONS_AND_VALUE_LABEL, 0)
        )

        self.__set_value_background_color()
        self.__set_text_color()

        colors.checkmark_container_background.trace(
            "w",
            lambda *args: self.__set_value_background_color()
        )

        colors.button_text.trace("w", lambda *args: self.__set_text_color())

        self._decrement_button.bind(
            event_names.LEFT_CLICK,
            self.__decrement_button_callback
        )

        self._increment_button.bind(
            event_names.LEFT_CLICK,
            self.__increment_button_callback
        )

    def set_background(self, color):
        _widgets_to_set_background_of = [
            self,
            self._heading,
            self._decrement_button,
            self._increment_button
        ]

        for _widget in _widgets_to_set_background_of:
            _widget.config(background=color)

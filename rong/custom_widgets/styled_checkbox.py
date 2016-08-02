import tkinter
from rong import images, fonts, event_names, utilities


class StyledCheckbox(tkinter.Frame):
    __CHECKBOX_SIZE = 40
    __CHECKMARK_CONTAINER_BORDER_WIDTH = 5
    __SPACE_BETWEEN_CHECKMARK_AND_LABEL = 20

    def __set_checkmark_state(self, *args):
        if self._variable.get():
            self._checkmark.pack()
        else:
            self._checkmark.pack_forget()

    def __init__(self, master, variable, text):
        super().__init__(master)

        self._variable = variable

        variable.trace("w", self.__set_checkmark_state)

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

        label = tkinter.Label(self, text=text, font=fonts.checkbox_font)
        label.pack()

        click_handler_arguments = (
            event_names.LEFT_CLICK,
            lambda *args: utilities.toggle_tkinter_boolean_variable(variable)
        )

        widgets_to_bind_click_handler_to = [
            self,
            self._checkmark,
            self._checkmark_container,
            label
        ]

        for _widget in widgets_to_bind_click_handler_to:
            _widget.bind(*click_handler_arguments)

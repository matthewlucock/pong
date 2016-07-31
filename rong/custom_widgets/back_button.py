from rong import event_names
from rong.screen_manager import screen_manager
from .styled_button import StyledButton

class BackButton(StyledButton):
    __TEXT = "Back"

    @staticmethod
    def __click_callback(*args):
        screen_manager.back()

    def __init__(self, master):
        super().__init__(master=master, text=self.__TEXT)
        self.bind(event_names.LEFT_CLICK, self.__click_callback)

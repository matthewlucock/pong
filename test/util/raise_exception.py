import unittest
from src.util import raise_exception


class TestRaiseException(unittest.TestCase):
    def test_raises_exception_by_default(self):
        with self.assertRaises(Exception):
            raise_exception(function_name="", message="")

    def test_raises_exception_specified(self):
        with self.assertRaises(ZeroDivisionError):
            raise_exception(
                exception=ZeroDivisionError,
                function_name="",
                message=""
            )

    def test_exception_message_includes_function_name_and_message(self):
        FUNCTION_NAME = "!"
        MESSAGE = "@"

        with self.assertRaises(Exception) as context_manager:
            raise_exception(
                exception=Exception,
                function_name=FUNCTION_NAME,
                message=MESSAGE
            )

        exception_message = context_manager.exception.args[0]
        self.assertIn(FUNCTION_NAME, exception_message)
        self.assertIn(MESSAGE, exception_message)

    def test_exception_message_includes_value_when_given(self):
        value = object()

        with self.assertRaises(Exception) as context_manager:
            raise_exception(
                exception=Exception,
                function_name="",
                message="",
                value=value
            )

        exception_message = context_manager.exception.args[0]
        self.assertIn(
            repr(value),
            exception_message,
        )

import unittest
import functools
from test import test_util


class TestValueValidatorBoolean(unittest.TestCase):
    __test_value = functools.partial(
        test_util.test_value_with_value_validator,
        method_name="boolean"
    )

    @staticmethod
    def __test_value_name(value_name):


    def test_errors_if_value_name_is_invalid(self):
        for value in test_util.EXAMPLE_DATA_TYPE_VALUES:
            if not isinstance(value, str):
                with self.assertRaises(TypeError):
                    self.__

    def test_errors_if_value_is_not_a_boolean(self):
        for value in test_util.EXAMPLE_DATA_TYPE_VALUES:
            if isinstance(value, bool):
                self.__test_value(value)
            else:
                with self.assertRaises(TypeError):
                    self.__test_value(value)

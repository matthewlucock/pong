import unittest
import functools
from test import test_util


class TestValueValidatorDictionary(unittest.TestCase):
    __test_value = functools.partial(
        test_util.test_value_with_value_validator,
        method_name="dictionary"
    )

    def test_errors_if_value_is_not_a_dictionary(self):
        for value in test_util.EXAMPLE_DATA_TYPE_VALUES:
            if isinstance(value, dict):
                self.__test_value(value)
            else:
                with self.assertRaises(TypeError):
                    self.__test_value(value)

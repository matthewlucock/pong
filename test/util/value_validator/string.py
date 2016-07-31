import unittest
import functools
from test import test_util


class TestValueValidatorString(unittest.TestCase):
    __test_value = functools.partial(
        test_util.test_value_with_value_validator,
        method_name="string"
    )

    __test_value_that_must_not_be_empty = functools.partial(
        __test_value,
        must_not_be_empty=True
    )

    __test_value_that_must_be_more_than_whitespace = functools.partial(
        __test_value,
        must_be_more_than_whitespace=True
    )

    def test_errors_if_must_not_be_empty_is_not_a_boolean(self):
        with self.assertRaises(TypeError):
            test_util.DUMMY_VALUE_VALIDATOR.string(
                value_name="",
                value="",
                must_not_be_empty=None
            )

    def test_errors_if_must_be_more_than_whitespace_is_not_a_boolean(self):
        with self.assertRaises(TypeError):
            test_util.DUMMY_VALUE_VALIDATOR.string(
                value_name="",
                value="",
                must_be_more_than_whitespace=None
            )

    def test_errors_if_value_is_not_a_string(self):
        for value in test_util.EXAMPLE_DATA_TYPE_VALUES:
            if isinstance(value, str):
                self.__test_value(value)
            else:
                with self.assertRaises(TypeError):
                    self.__test_value(value)

    def test_must_not_be_empty(self):
        for value in test_util.EXAMPLE_DATA_TYPE_VALUES:
            if not isinstance(value, str):
                continue

            if value:
                self.__test_value_that_must_not_be_empty(value)
            else:
                with self.assertRaises(ValueError):
                    self.__test_value_that_must_not_be_empty(value)

    def test_must_be_more_than_whitespace(self):
        for value in test_util.EXAMPLE_DATA_TYPE_VALUES:
            if not isinstance(value, str):
                continue

            if value.strip():
                self.__test_value_that_must_be_more_than_whitespace(value)
            else:
                with self.assertRaises(ValueError):
                    self.__test_value_that_must_be_more_than_whitespace(value)

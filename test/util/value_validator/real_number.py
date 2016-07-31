import unittest
import functools
import numbers
from test import test_util


class TestValueValidatorRealNumber(unittest.TestCase):
    __test_value = functools.partial(
        test_util.test_value_with_value_validator,
        method_name="real_number"
    )

    __test_value_that_must_be_positive = functools.partial(
        __test_value,
        must_be_positive=True
    )

    def test_errors_if_must_be_positive_is_not_a_boolean(self):
        with self.assertRaises(TypeError):
            test_util.DUMMY_VALUE_VALIDATOR.real_number(
                value_name="",
                value=1,
                must_be_positive=None
            )

    def test_errors_if_value_is_not_a_real_number(self):
        for value in test_util.EXAMPLE_DATA_TYPE_VALUES:
            if isinstance(value, numbers.Real):
                self.__test_value(value)
            else:
                with self.assertRaises(TypeError):
                    self.__test_value(value)

    def test_must_be_positive(self):
        for value in test_util.EXAMPLE_DATA_TYPE_VALUES:
            if not isinstance(value, numbers.Real):
                continue

            if value > 0:
                self.__test_value_that_must_be_positive(value)
            else:
                with self.assertRaises(ValueError):
                    self.__test_value_that_must_be_positive(value)

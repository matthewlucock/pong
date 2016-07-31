from src.util import ValueValidator

DUMMY_FUNCTION = lambda: None

EXAMPLE_DATA_TYPE_VALUES = [
    "",
    " ",
    "_",
    0,
    1,
    1/3,
    -1,
    True,
    False,
    [],
    (),
    {},
    DUMMY_FUNCTION,
    object()
]

DUMMY_VALUE_VALIDATOR = ValueValidator(
    function_name="",
    descriptions={"": ""}
)

def test_value_with_value_validator(method_name, value, **kwargs):
    kwargs.update({
        "value_name": "",
        "value": value
    })

    getattr(DUMMY_VALUE_VALIDATOR, method_name)(**kwargs)

def test_value_name_with_value_validator(method_name, value_name, value):
    getattr(DUMMY_VALUE_VALIDATOR, method_name)(
        value_name=value_name,
        value=value
    )

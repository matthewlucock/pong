import collections
from rong import utilities

Direction = collections.namedtuple(
    typename="Direction",
    field_names=["vector", "left_half_key", "right_half_key"]
)

up = Direction(
    vector=utilities.Vector(y=-1),
    left_half_key="w",
    right_half_key="i"
)

down = Direction(
    vector=utilities.Vector(y=1),
    left_half_key="s",
    right_half_key="k"
)

left = Direction(
    vector=utilities.Vector(x=-1),
    left_half_key="a",
    right_half_key="j"
)

right = Direction(
    vector=utilities.Vector(x=1),
    left_half_key="d",
    right_half_key="l"
)

Rotation = collections.namedtuple(
    typename = "Rotation",
    field_names = ["rotation", "left_half_key", "right_half_key"]
)

clock_wise = Rotation(
    rotation = 1,
    left_half_key = "e",
    right_half_key = "o"
)

anti_clock_wise = Rotation(
    rotation = -1,
    left_half_key = "q",
    right_half_key = "u"
)

_rotations = [
    clock_wise,
    anti_clock_wise
]

_directions = [
    up,
    down,
    left,
    right
]

def get_direction_from_keys(keys, in_right_half):
    resulting_direction = utilities.Vector(0, 0)

    for direction in _directions:
        for key in keys:
            if (
                    in_right_half and key == direction.right_half_key \
                    or not in_right_half and key == direction.left_half_key
            ):
                resulting_direction += direction.vector

    resulting_direction.normalise()
    return resulting_direction

def get_rotation_from_keys(keys, in_right_half):
    resulting_rotation = 0

    for rotation in _rotations:
        for key in keys:
            if (
                    in_right_half and key == rotation.right_half_key
                    or not in_right_half and key == rotation.left_half_key
            ):
                resulting_rotation += rotation.rotation

    return resulting_rotation
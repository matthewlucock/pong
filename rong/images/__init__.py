import PIL
import PIL.ImageTk

_IMAGE_PATH = "rong/images/{}.png"
_SPRITE_PATH = _IMAGE_PATH.format("sprites/{}")

RIGHT_POINTING_ARROW = PIL.Image.open(_IMAGE_PATH.format("arrow"))
LEFT_POINTING_ARROW = RIGHT_POINTING_ARROW.rotate(180)
RIGHT_POINTING_BLACK_ARROW = PIL.Image.open(_IMAGE_PATH.format("arrow_black"))
LEFT_POINTING_BLACK_ARROW = RIGHT_POINTING_BLACK_ARROW.rotate(180)
CHECKMARK = PIL.Image.open(_IMAGE_PATH.format("checkmark"))
BLACK_CHECKMARK = PIL.Image.open(_IMAGE_PATH.format("checkmark_black"))
PAUSE_GLYPH = PIL.Image.open(_IMAGE_PATH.format("pause"))
BLACK_PAUSE_GLYPH = PIL.Image.open(_IMAGE_PATH.format("pause_black"))

TKINTER_USABLE_RIGHT_POINTING_ARROW = PIL.ImageTk.PhotoImage(
    RIGHT_POINTING_ARROW
)

TKINTER_USABLE_LEFT_POINTING_ARROW = PIL.ImageTk.PhotoImage(
    LEFT_POINTING_ARROW
)

TKINTER_USABLE_RIGHT_POINTING_BLACK_ARROW = PIL.ImageTk.PhotoImage(
    RIGHT_POINTING_BLACK_ARROW
)

TKINTER_USABLE_LEFT_POINTING_BLACK_ARROW = PIL.ImageTk.PhotoImage(
    LEFT_POINTING_BLACK_ARROW
)

TKINTER_USABLE_CHECKMARK = PIL.ImageTk.PhotoImage(CHECKMARK)
TKINTER_USABLE_BLACK_CHECKMARK = PIL.ImageTk.PhotoImage(BLACK_CHECKMARK)

TKINTER_USEABLE_PAUSE_GLYPH = PIL.ImageTk.PhotoImage(PAUSE_GLYPH)
TKINTER_USEABLE_BLACK_PAUSE_GLYPH = PIL.ImageTk.PhotoImage(BLACK_PAUSE_GLYPH)

_LIST_OF_SPRITES = [
    "ball_speed_boost",
    "ball_speed_reduction",
    "engorgement",
    "ensmallment",
    "lock_opponent_position",
    "lock_opponent_rotation",
    "multiple_balls",
    "other_narrowment",
    "other_paddle_speed_reduction",
    "own_paddle_speed_boost",
    "self_widenment"
]

sprites = {}

for _sprite_name in _LIST_OF_SPRITES:
    _image = PIL.Image.open(_SPRITE_PATH.format(_sprite_name))
    sprites[_sprite_name] = PIL.ImageTk.PhotoImage(_image)

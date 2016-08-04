import winsound
from rong.window import window
from rong import game_variables
from rong.screen_manager import screen_manager
from rong.screens.main_screen import main_screen
from rong.screens.game_screen import game_screen

window.protocol(
    "WM_DELETE_WINDOW",
    lambda: game_variables.application_has_exited.set(True)
)

# winsound.PlaySound("rong/audio.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

screen_manager.main_screen = main_screen
screen_manager.game_screen = game_screen
screen_manager.change_screen(main_screen)

while True:
    if game_variables.application_has_exited.get():
        break

    window.update()

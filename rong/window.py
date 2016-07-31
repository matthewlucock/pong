import tkinter

WINDOW_DIMENSIONS = (1280, 720)

window = tkinter.Tk()

window.title("Rong")
window.geometry(
    "{}x{}".format(*WINDOW_DIMENSIONS)
)
window.resizable(width=False, height=False)

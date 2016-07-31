from tkinter import BooleanVar, StringVar, IntVar

application_has_exited = BooleanVar()

#music_enabled = BooleanVar()
high_contrast_mode_enabled = BooleanVar()

game_mode = StringVar()
game_is_paused = BooleanVar()

selected_campaign_level = IntVar()
versus_ai_difficulty = IntVar()
power_ups_enabled = BooleanVar()
free_movement_enabled = BooleanVar()

#music_enabled.set(True)
selected_campaign_level.set(5)
versus_ai_difficulty.set(5)
power_ups_enabled.set(True)

from time import perf_counter

class Clock:
    def __init__(self):
        perf_counter()
        self.update()

    def calculate_delta_time(self):
        return perf_counter() - self._time_of_last_frame

    def update(self):
        self._time_of_last_frame = perf_counter()

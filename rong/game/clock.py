from time import perf_counter

class Clock:
    def __init__(self):
        perf_counter()
        self._time_of_last_call = 0

    def calculate_delta_time(self):
        time_since_first_call = perf_counter()
        time_since_last_call = time_since_first_call - self._time_of_last_call
        self._time_of_last_call = time_since_first_call
        return time_since_last_call

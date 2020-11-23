class Dandere2xController:
    def __init__(self):
        self._is_alive = True
        self._current_frame = 1

    def update_frame_count(self, set_frame: int):
        self._current_frame = set_frame

    def get_current_frame(self):
        return self._current_frame

    def kill(self):
        self._is_alive = False

    def is_alive(self):
        return self._is_alive
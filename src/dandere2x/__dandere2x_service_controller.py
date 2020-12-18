class Dandere2xController:
    """
    A simple thread-safe (not really) way of communicating to different parts of dandere2x what frame / the health
    status of the current dandere2x instance.
    """

    def __init__(self):
        self._current_frame = 1

    def update_frame_count(self, set_frame: int):
        self._current_frame = set_frame

    def get_current_frame(self):
        return self._current_frame

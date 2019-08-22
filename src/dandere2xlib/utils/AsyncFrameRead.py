import threading
from wrappers.frame import Frame


class AsyncFrameRead(threading.Thread):

    def __init__(self, input_image: str):
        # calling superclass init
        threading.Thread.__init__(self)
        self.input_image = input_image
        self.loaded_image = Frame()
        self.load_complete = False

    def run(self):
        self.loaded_image.load_from_string_wait(self.input_image)
        self.load_complete = True

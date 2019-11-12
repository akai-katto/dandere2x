import threading

from wrappers.frame.frame import Frame


class AsyncFrameRead(threading.Thread):
    """
    Read an image asynchronously
    """

    def __init__(self, input_image: str):
        # calling superclass init
        threading.Thread.__init__(self)
        self.input_image = input_image
        self.loaded_image = Frame()
        self.load_complete = False

    def run(self):
        self.loaded_image.load_from_string_wait(self.input_image)
        self.load_complete = True


class AsyncFrameWrite(threading.Thread):
    """
    Write an image asynchronously
    """

    def __init__(self, image: Frame, output_image: str):
        # calling superclass init
        threading.Thread.__init__(self)
        self.image = image
        self.output_image = output_image

    def run(self):
        self.image.save_image(out_location=self.output_image)

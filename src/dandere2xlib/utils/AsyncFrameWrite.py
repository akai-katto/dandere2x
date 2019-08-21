import threading
from wrappers.frame import Frame


class AsyncFrameWrite(threading.Thread):

    def __init__(self, image: Frame, output_image: str):
        # calling superclass init
        threading.Thread.__init__(self)
        self.image = image
        self.output_image = output_image

    def run(self):
        self.image.save_image(out_location=self.output_image)


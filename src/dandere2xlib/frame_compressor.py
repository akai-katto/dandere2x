import os
import threading

from context import Context
from dandere2xlib.utils.thread_utils import CancellationToken
from wrappers.frame.frame import Frame


class CompressFrames(threading.Thread):

    def __init__(self, context: Context):

        # load context
        self.inputs_dir = context.input_frames_dir
        self.frame_count = context.frame_count
        self.quality_moving_ratio = context.quality_moving_ratio
        self.compressed_static_dir = context.compressed_static_dir
        self.compressed_moving_dir = context.compressed_moving_dir
        self.quality_minimum = context.quality_minimum
        self.extension_type = context.extension_type
        self.start_frame = 1

        # threading member variables
        self.cancel_token = CancellationToken()
        self.alive = True
        self._stopevent = threading.Event()
        threading.Thread.__init__(self, name="CompressFramesThread")

    def join(self, timeout=None):
        threading.Thread.join(self, timeout)

    def kill(self):
        self.cancel_token.cancel()
        self.alive = False
        self._stopevent.set()

    def set_start_frame(self, start_frame: int):
        self.start_frame = start_frame

    def run(self):
        # start from 1 because ffmpeg's extracted frames starts from 1
        for x in range(self.start_frame, self.frame_count + 1):

            # loading files area
            frame = Frame()
            frame.load_from_string_wait(self.inputs_dir + "frame" + str(x) + self.extension_type, self.cancel_token)

            # stop if thread was killed
            if not self.alive:
                return

            # if the compressed frame already exists, don't compress it
            if os.path.exists(self.compressed_static_dir + "compressed_" + str(x) + ".jpg"):
                continue

            frame.save_image_quality(self.compressed_static_dir + "compressed_" + str(x) + ".jpg",
                                     self.quality_minimum)
            frame.save_image_quality(self.compressed_moving_dir + "compressed_" + str(x) + ".jpg",
                                     int(self.quality_minimum * self.quality_moving_ratio))

import cv2


class ProgressiveFramesExtractorCV2:
    """
    Temporally extract frames from a video each time next_frame is called.

    Saves into dandere2x's inputs DIR.
    """

    def __init__(self, context):
        self.cap = cv2.VideoCapture(context.input_file)
        self.input_frames_dir = context.input_frames_dir
        self.count = 1

    # TODO: need to apply core d2x filters # FIXED: FFMPEG WORKAROUND
    def next_frame(self):
        """
        Call and save the next frame.
        """

        success, image = self.cap.read()

        if success:
            cv2.imwrite(self.input_frames_dir + "frame%s.jpg" % self.count, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
            self.count += 1

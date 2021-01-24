import cv2

from dandere2x.dandere2xlib.utils.dandere2x_utils import rename_file_wait


class ProgressiveFramesExtractorCV2:
    """
    Temporally extract frames from a video each time next_frame is called.
    Saves into dandere2x's inputs DIR.
    """

    def __init__(self, input_video: str, extracted_frames_dir: str, compressed_frames_dir: str,
                 compressed_quality: int):

        self.input_video = input_video
        self.extracted_frames_dir = extracted_frames_dir
        self.compressed_frames_dir = compressed_frames_dir
        self.compressed_quality = compressed_quality
        self.cap = cv2.VideoCapture(self.input_video)

        self.count = 1

    def extract_frames_to(self, stop_frame: int):

        for x in range(1, stop_frame):
            self.next_frame()

    def release_capture(self):

        #todo, investigate / remove this try catch block with an actual solution
        try:
            # Closes all the frames
            self.cap.release()
            cv2.destroyAllWindows()

        except cv2.error:
            print("cv2 error caught - this behaviour is unexpected by the developer, but testing to see if this is"
                  " a potential duct-tape fix.")

    # todo, need to find a fix for "stuck at 99%" error, or getting stuck prematurely.
    def next_frame(self):
        """ Call and save the next frame. """

        success = False
        while not success:
            success, image = self.cap.read()

        if success:
            cv2.imwrite(self.extracted_frames_dir + "frame_temp_%s.jpg" % self.count, image,
                        [cv2.IMWRITE_JPEG_QUALITY, 100])
            cv2.imwrite(self.compressed_frames_dir + "compressed_temp_%s.jpg" % self.count, image,
                        [cv2.IMWRITE_JPEG_QUALITY, self.compressed_quality])

            rename_file_wait(self.extracted_frames_dir + "frame_temp_%s.jpg" % self.count,
                             self.extracted_frames_dir + "frame%s.jpg" % self.count)

            rename_file_wait(self.compressed_frames_dir + "compressed_temp_%s.jpg" % self.count,
                             self.compressed_frames_dir + "compressed_%s.jpg" % self.count)

            self.count += 1

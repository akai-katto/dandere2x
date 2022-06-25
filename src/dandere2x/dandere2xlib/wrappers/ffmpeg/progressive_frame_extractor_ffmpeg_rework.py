from pathlib import Path

import cv2

from dandere2x.dandere2xlib.utils.dandere2x_utils import rename_file_wait
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg import apply_noise_to_image
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg_progressive_frame_extractor import VideoFrameExtractor
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffprobe import get_width_height

class ProgressiveFramesExtractorFFMPEG:
    """
    Temporally extract frames from a video each time next_frame is called.
    Saves into dandere2x's inputs DIR.
    """

    def __init__(self,
                 input_video: str,
                 extracted_frames_dir: str,
                 compressed_frames_dir: str,
                 compressed_quality: int,
                 block_size: int,
                 output_options_original: dict):

        ffprobe_path = load_executable_paths_yaml()['ffprobe']

        self.input_video = input_video
        self.extracted_frames_dir = extracted_frames_dir
        self.compressed_frames_dir = compressed_frames_dir

        self.compressed_quality = compressed_quality

        width, height = get_width_height(ffprobe_dir=ffprobe_path, input_video=input_video)
        self.cap = VideoFrameExtractor(Path(input_video), width, height, block_size, output_options_original)

        self.ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

        self.count = 1

    def extract_frames_to(self, stop_frame: int):

        for x in range(1, stop_frame):
            self.next_frame()

    def release_capture(self):
        pass
        # #todo, investigate / remove this try catch block with an actual solution
        # try:
        #     # Closes all the frames
        #     self.cap.release()
        #     cv2.destroyAllWindows()
        #
        # except cv2.error:
        #     print("cv2 error caught - this behaviour is unexpected by the developer, but testing to see if this is"
        #           " a potential duct-tape fix.")

    # todo, need to find a fix for "stuck at 99%" error, or getting stuck prematurely.
    def next_frame(self):
        """ Call and save the next frame. """

        success = False
        image = self.cap.get_frame()

        temp_image = self.extracted_frames_dir + "frame_temp_%s.png" % self.count
        final_image = self.extracted_frames_dir + "frame%s.png" % self.count

        image.save(Path(temp_image))

        rename_file_wait(temp_image, final_image)

        self.count += 1

import threading
import time
import uuid
from pathlib import Path

from dandere2x.dandere2xlib.utils.dandere2x_utils import rename_file_wait
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.progressive_frame_extractor._ffmpeg_video_frame_extractor import \
    FFMpegVideoFrameExtractor, D2xFrame
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffprobe import get_width_height


class ProgressiveFrameExtractor:
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
        ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

        self.input_video = input_video
        self.extracted_frames_dir = extracted_frames_dir
        self.compressed_frames_dir = compressed_frames_dir

        self.compressed_quality = compressed_quality

        width, height = get_width_height(ffprobe_dir=ffprobe_path, input_video=input_video)
        self.cap = FFMpegVideoFrameExtractor(Path(ffmpeg_path), Path(input_video), width, height, block_size, output_options_original)

        self.ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

        self.count = 1

    def extract_frames_to(self, stop_frame: int):
        for x in range(1, stop_frame):
            self.next_frame()

    # todo, need to find a fix for "stuck at 99%" error, or getting stuck prematurely.
    def next_frame(self):
        """ Call and save the next frame. """

        success = False
        image = self.cap.get_frame()

        temp_image = self.extracted_frames_dir + str(uuid.uuid4()) + "frame_temp_%s.png" % self.count
        final_image = self.extracted_frames_dir + "frame%s.png" % self.count

        threading.Thread(target=self.save_asyncable, args=(image, temp_image, final_image,)).start()

        self.count += 1

    @staticmethod
    def save_asyncable(image: D2xFrame, temp_image:str,  final_image: str):
        image.save(Path(temp_image))
        rename_file_wait(temp_image, final_image)
from time import sleep

import av

from threading import Thread
from dandere2x.dandere2xlib.utils.dandere2x_utils import rename_file_wait
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg import apply_noise_to_image


class ProgressiveFramesExtractorAV:
    """
    Temporally extract frames from a video each time next_frame is called.
    Saves into dandere2x's inputs DIR.
    """

    def __init__(self,
                 input_video: str,
                 extracted_frames_dir: str,
                 compressed_frames_dir: str,
                 compressed_quality: int):

        self.input_video = input_video
        self.extracted_frames_dir = extracted_frames_dir
        self.compressed_frames_dir = compressed_frames_dir
        self.count = 1
        self.extracted_count = 1

        thread_start = Thread(target=self._start_av_thread)
        thread_start.start()

    def extract_frames_to(self, stop_frame: int):

        for x in range(1, stop_frame):
            self.next_frame()

    def _start_av_thread(self):
        container = av.open(self.input_video)

        for frame in container.decode(video=0):
            temp_image = self.extracted_frames_dir + "frame_temp_%s.png" % self.extracted_count
            final_image = self.extracted_frames_dir + "frame%s.png" % self.extracted_count

            while self.count < self.extracted_count:
                sleep(0.01)

            frame.to_image().save(temp_image)
            self.extracted_count += 1
            Thread(target=rename_file_wait, args=(temp_image, final_image)).start()



    # todo, need to find a fix for "stuck at 99%" error, or getting stuck prematurely.
    def next_frame(self):
        while self.extracted_count < self.count:
            sleep(0.01)

        self.count += 1

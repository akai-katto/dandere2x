import logging
import subprocess
import time

import psutil

from dandere2xlib.utils.dandere2x_utils import file_exists, file_is_empty
from dandere2xlib.utils.yaml_utils import get_options_from_section
from wrappers.frame.frame import Frame


class ProgressiveFramesExtractorFFMPEG:
    """
    Temporally extract frames from a video each time next_frame is called.
    This is achieved by freezing the FFMPEG process responsible for extracting frames when the needed frame appears,
    and unfreezing it when we need to extract another.

    Saves into dandere2x's 'inputs' DIR.
    """

    def __init__(self, context, input_file):
        self.context = context
        self.input_frames_dir = context.input_frames_dir
        self.count = 1
        self.input_frames_dir = context.input_frames_dir
        self.extension_type = context.extension_type
        self.input_file = input_file

        self.output_file = self.input_frames_dir + "frame%01d" + self.extension_type
        self.logger = logging.getLogger(__name__)
        self.frame_rate = context.frame_rate

        self.P = None
        self.pause_resume = None

    def start_task(self):

        extract_frames_command = [self.context.ffmpeg_dir,
                                  "-hwaccel", self.context.hwaccel,
                                  "-i", self.input_file]

        extract_frames_options = \
            get_options_from_section(self.context.config_yaml["ffmpeg"]["video_to_frames"]['output_options'],
                                     ffmpeg_command=True)

        for element in extract_frames_options:
            extract_frames_command.append(element)

        extract_frames_command.append("-r")
        extract_frames_command.append(str(self.frame_rate))

        extract_frames_command.extend([self.output_file])

        self.logger.info("extracting frames")

        console_output = open(self.context.console_output_dir + "ffmpeg_extract_frames_console.txt", "w")
        console_output.write(str(extract_frames_command))

        self.P = subprocess.Popen(extract_frames_command, shell=False,
                                  stderr=console_output, stdout=console_output)
        self.pause_resume = psutil.Process(self.P.pid)
        self.pause_resume.suspend()

    def kill_task(self):
        self.pause_resume.kill()

    def extract_frames_to(self, stop_frame: int):

        self.count = stop_frame

        # Resume the thread in order to produce a new frame.
        self.pause_resume.resume()
        # Although the file may exist, there are niche conditions in which the file on disk is
        # not processable. Make sure the image is proccessible before killing the signal.
        while not file_exists(self.input_frames_dir + "frame" + str(self.count) + self.extension_type):
            time.sleep(.00001)

        while file_is_empty(self.input_frames_dir + "frame" + str(self.count) + self.extension_type):
            time.sleep(.00001)

    def next_frame(self):
        """
        Call and save the next frame.
        """

        # FFMPEG extracts images pretty fast depending on hardware, so in some cases although we've already
        # we've only instructed ffmpeg to extract N frames, N + k (for some k) may already be extracted.
        if file_exists(self.input_frames_dir + "frame" + str(self.count) + self.extension_type):
            self.count += 1
            return

        # Resume the thread in order to produce a new frame.
        self.pause_resume.resume()

        # Although the file may exist, there are niche conditions in which the file on disk is
        # not processable. Make sure the image is proccessible before killing the signal.
        while not file_exists(self.input_frames_dir + "frame" + str(self.count) + self.extension_type):
            time.sleep(.00001)

        while file_is_empty(self.input_frames_dir + "frame" + str(self.count) + self.extension_type):
            time.sleep(.00001)

        # make sure the image is actually loadable before stopping the ffmpeg thread by using the wait function.
        # frame has.
        f = Frame()
        f.load_from_string_wait(self.input_frames_dir + "frame" + str(self.count) + self.extension_type)

        # Pause the thread.
        self.pause_resume.suspend()

        self.count += 1

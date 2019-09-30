from dandere2xlib.utils.yaml_utils import get_options_from_section
from dandere2xlib.utils.dandere2x_utils import wait_on_file
from wrappers.ffmpeg.ffmpeg import migrate_tracks

import time
import subprocess
import threading


class Pipe():

    def __init__(self, context):

        print("\n    WARNING: EXPERIMENTAL FFMPEG PIPING IS ENABLED\n")

        self.context = context

        # load variables from context
        self.workspace = self.context.workspace
        self.upscaled_dir = self.context.residual_upscaled_dir
        self.compressed_static_dir = self.context.compressed_static_dir
        self.compressed_moving_dir = self.context.compressed_moving_dir
        self.input_frames_dir = self.context.input_frames_dir
        self.merged_dir = self.context.merged_dir
        self.residual_data_dir = self.context.residual_data_dir
        self.pframe_data_dir = self.context.pframe_data_dir
        self.correction_data_dir = self.context.correction_data_dir
        self.fade_data_dir = self.context.fade_data_dir
        self.frame_count = self.context.frame_count
        self.extension_type = self.context.extension_type
        self.waifu2x_type = self.context.waifu2x_type

        # pipe stuff
        self.pipe_running = 1
        self.images_to_pipe = []

        self.nosound_file = self.context.nosound_file
        self.frame_rate = str(self.context.frame_rate)
        self.input_file = self.context.input_file
        self.output_file = self.context.output_file
        self.ffmpeg_dir = self.context.ffmpeg_dir

        ffmpeg_pipe_command = [self.ffmpeg_dir, "-r", self.frame_rate]

        options = get_options_from_section(context.config_yaml["ffmpeg"]["pipe_video"]['output_options'],
                                            ffmpeg_command=True)

        for item in options:
            ffmpeg_pipe_command.append(item)

        ffmpeg_pipe_command.append("-r")
        ffmpeg_pipe_command.append(self.frame_rate)
        ffmpeg_pipe_command.append(self.nosound_file)

        self.ffmpeg_pipe_subprocess = subprocess.Popen(ffmpeg_pipe_command, stdin=subprocess.PIPE)
        threading.Thread(target=self.__write_to_pipe).start()

    def save(self, frame):  # '_' to ignore the "x" var needed in AsyncWrite on merge.py

        # Write the image directly into ffmpeg pipe
        # by adding image to image_to_pipe list
        # kinda similar to AsyncFrameWrite

        while True:
            if len(self.images_to_pipe) < 10:  # buffer limit
                self.images_to_pipe.append(frame)
                break
            time.sleep(0.05)

    def __close(self):
        self.ffmpeg_pipe_subprocess.stdin.close()
        self.ffmpeg_pipe_subprocess.wait()

    def __write_to_pipe(self):
        while self.pipe_running:
            if len(self.images_to_pipe) > 0:
                img = self.images_to_pipe.pop(0).get_pil_image()  # get the first image and remove it from list
                img.save(self.ffmpeg_pipe_subprocess.stdin, format="jpeg", quality=100)
            time.sleep(0.05)

        # close and finish audio file

        print("\n  Closing FFMPEG as encode finished...")

        self.__close()

    def wait_finish_stop_pipe(self):

        print("\n    Waiting for the ffmpeg-pipe-encode buffer list to end....")

        while self.images_to_pipe:
            time.sleep(0.05)


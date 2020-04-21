import subprocess
import threading
import time

from dandere2xlib.utils.yaml_utils import get_options_from_section


class Pipe():
    """
    The pipe class allows images (Frame.py) to be processed into a video directly. It does this by "piping"
    images to ffmpeg, thus removing the need for storing the processed images onto the disk.
    """

    def __init__(self, context, output_no_sound: str):
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
        self.waifu2x_type = self.context.waifu2x_type

        # How many images to have maximum in a buffer at a given time.
        self.buffer_limit = 20
        self.pipe_running = True
        self.images_to_pipe = []

        self.nosound_file = output_no_sound
        self.frame_rate = str(self.context.frame_rate)
        self.dar = self.context.dar
        self.input_file = self.context.input_file
        self.output_file = self.context.output_file
        self.ffmpeg_dir = self.context.ffmpeg_dir

        # Create the piping command
        self.ffmpeg_pipe_command = [self.ffmpeg_dir, "-r", self.frame_rate]

        options = get_options_from_section(context.config_yaml["ffmpeg"]["pipe_video"]['output_options'],
                                           ffmpeg_command=True)

        for item in options:
            self.ffmpeg_pipe_command.append(item)

        self.ffmpeg_pipe_command.append("-r")
        self.ffmpeg_pipe_command.append(self.frame_rate)

        if self.dar:
            self.ffmpeg_pipe_command.append("-vf")
            self.ffmpeg_pipe_command.append("setdar=" + self.dar.replace(":", "/"))

        self.ffmpeg_pipe_command.append(self.nosound_file)

        self.ffmpeg_pipe_subprocess = None

        # thread variables

        self.thread_alive = True

    def join_ffmpeg_subprocess(self):
        print("waiting for pipe join")
        self.ffmpeg_pipe_subprocess.wait()
        print("pipe join done")

    def kill_thread(self):
        self.thread_alive = False

    def start_pipe_thread(self):
        console_output = open(self.context.console_output_dir + "pipe_output.txt", "w")
        self.ffmpeg_pipe_subprocess = subprocess.Popen(self.ffmpeg_pipe_command, stdin=subprocess.PIPE,
                                                       stdout=console_output)
        threading.Thread(target=self.__write_to_pipe, name="pipehtread").start()

    # todo: Implement this without a 'while true'
    def save(self, frame):
        """
        Try to add an image to image_to_pipe buffer. If there's too many images in the buffer,
        simply wait until the buffer clears.
        """
        while True:
            if len(self.images_to_pipe) < self.buffer_limit:
                self.images_to_pipe.append(frame)
                break
            time.sleep(0.05)

    def wait_finish_stop_pipe(self):
        """
        Prevent another program from continuing until all the images have been written to the pipe.
        """

        print("\n    Waiting for the ffmpeg-pipe-encode buffer list to end....")

        while len(self.images_to_pipe) > 0 and self.thread_alive:
            time.sleep(0.05)

        self.pipe_running = False

    def __close(self):
        self.ffmpeg_pipe_subprocess.stdin.close()
        self.ffmpeg_pipe_subprocess.wait()

    def __write_to_pipe(self):
        """
        Continually pop images from the buffer into the piped video while there are still images to be piped.
        """

        while self.pipe_running and self.thread_alive:
            if len(self.images_to_pipe) > 0:
                img = self.images_to_pipe.pop(0).get_pil_image()  # get the first image and remove it from list
                img.save(self.ffmpeg_pipe_subprocess.stdin, format="jpeg", quality=100)
            time.sleep(0.05)

        print("\n  Closing FFMPEG as encode finished...")

        self.__close()

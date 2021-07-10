import subprocess
import threading
import time

from colorlog import logging

from dandere2x.dandere2x_service.dandere2x_service_context import Dandere2xServiceContext
from dandere2x.dandere2x_service.dandere2x_service_controller import Dandere2xController
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml, get_options_from_section


class Pipe(threading.Thread):
    """
    The pipe class allows images (Frame.py) to be processed into a video directly. It does this by "piping"
    images to ffmpeg, thus removing the need for storing the processed images onto the disk.
    """

    def __init__(self, output_no_sound: str, context: Dandere2xServiceContext, controller: Dandere2xController):
        threading.Thread.__init__(self, name="Pipe Thread")

        # load context
        self.context = context
        self.controller = controller
        self.output_no_sound = output_no_sound
        self.log = logging.getLogger(name=self.context.service_request.input_file)

        # class specific
        self.ffmpeg_pipe_subprocess = None
        self.alive = False
        self.images_to_pipe = []
        self.buffer_limit = 20
        self.lock_buffer = False

    def kill(self) -> None:
        self.log.info("Kill called.")
        self.alive = False

    def run(self) -> None:
        self.log.info("Run Called")

        self.alive = True
        self._setup_pipe()

        # keep piping images to ffmpeg while this thread is supposed to be kept alive.
        while self.alive:
            if len(self.images_to_pipe) > 0:
                img = self.images_to_pipe.pop(0).get_pil_image()  # get the first image and remove it from list
                img.save(self.ffmpeg_pipe_subprocess.stdin, format="jpeg", quality=100)
            else:
                time.sleep(0.1)

        # if the thread is killed for whatever reason, finish writing the remainder of the images to the video file.
        while self.images_to_pipe:
            pil_image = self.images_to_pipe.pop(0).get_pil_image()
            pil_image.save(self.ffmpeg_pipe_subprocess.stdin, format="jpeg", quality=100)

        self.ffmpeg_pipe_subprocess.stdin.close()
        self.ffmpeg_pipe_subprocess.wait()

        # ensure thread is dead (can be killed with controller.kill() )
        self.alive = False

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

    def _setup_pipe(self) -> None:
        self.log.info("Setting up pipe Called")
        # load variables..
        output_no_sound = self.output_no_sound
        frame_rate = str(self.context.frame_rate)
        output_no_sound = output_no_sound
        ffmpeg_dir = load_executable_paths_yaml()['ffmpeg']
        dar = self.context.video_settings.dar

        # constructing the pipe command...
        ffmpeg_pipe_command = [ffmpeg_dir]

        # no walrus operator sad
        hw_accel = self.context.service_request.output_options["ffmpeg"]["pipe_video"]["-hwaccel"]
        if hw_accel is not None:
            ffmpeg_pipe_command.append("-hwaccel")
            ffmpeg_pipe_command.append(hw_accel)

        ffmpeg_pipe_command.extend(["-r", frame_rate])

        options = get_options_from_section(
            self.context.service_request.output_options["ffmpeg"]["pipe_video"]['output_options'],
            ffmpeg_command=True)
        for item in options:
            ffmpeg_pipe_command.append(item)

        ffmpeg_pipe_command.append("-r")
        ffmpeg_pipe_command.append(frame_rate)

        ffmpeg_pipe_command.append(output_no_sound)

        # Starting the Pipe Command
        console_output = open(self.context.console_output_dir + "pipe_output.txt", "w")
        console_output.write(str(ffmpeg_pipe_command))

        self.log.info("ffmpeg_pipe_command %s" % str(ffmpeg_pipe_command))
        self.ffmpeg_pipe_subprocess = subprocess.Popen(ffmpeg_pipe_command, stdin=subprocess.PIPE,
                                                       stdout=console_output)

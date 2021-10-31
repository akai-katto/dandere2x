import logging
import os
from pathlib import Path

from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.videosettings import VideoSettings


class Dandere2xServiceContext:

    def __init__(self, service_request: Dandere2xServiceRequest):
        """

        Creates struct-like object that serves as a set of constants and directories dandere2x will use. Once this is
        instantiated, it's to be treated as 'effectively final' meaning that none of the variables will
        change after they're declared.

        Most dandere2x-core functions will require a Dandere2xServiceContext object in order for it to run.

        Args:
            service_request: A service_request, which may be produced by the program or the user.
        """

        self.service_request = service_request

        # Directories and Paths
        self.input_frames_dir: Path = service_request.workspace / "inputs"
        self.noised_input_frames_dir: Path = service_request.workspace / "noised_inputs"
        self.residual_images_dir: Path = service_request.workspace / "residual_images"
        self.residual_upscaled_dir: Path = service_request.workspace / "residual_upscaled"
        self.residual_data_dir: Path = service_request.workspace / "residual_data"
        self.pframe_data_dir: Path = service_request.workspace / "pframe_data"
        self.merged_dir: Path = service_request.workspace / "merged"
        self.fade_data_dir: Path = service_request.workspace / "fade_data"
        self.debug_dir = service_request.workspace / "debug"
        self.console_output_dir: Path = service_request.workspace / "console_output"
        self.compressed_static_dir: Path = service_request.workspace / "compressed_static"
        self.encoded_dir: Path = service_request.workspace / "encoded"
        self.temp_image_folder: Path = service_request.workspace / "temp_image_folder"
        self.log_dir: Path = service_request.workspace / "log_dir"

        self.directories = {self.input_frames_dir,
                            self.noised_input_frames_dir,
                            self.residual_images_dir,
                            self.residual_upscaled_dir,
                            self.merged_dir,
                            self.residual_data_dir,
                            self.pframe_data_dir,
                            self.debug_dir,
                            self.console_output_dir,
                            self.compressed_static_dir,
                            self.fade_data_dir,
                            self.encoded_dir,
                            self.temp_image_folder,
                            self.log_dir}

        ffprobe_path = load_executable_paths_yaml()['ffprobe']
        video_settings = VideoSettings(ffprobe_path, self.service_request.input_file)
        self.video_settings = video_settings
        self.width, self.height = video_settings.width, video_settings.height
        self.frame_count = video_settings.frame_count
        self.frame_rate = video_settings.frame_rate

        # todo static-ish settings < add to a yaml somewhere >
        self.bleed = self.service_request.output_options["dandere2x"]["bleed"]
        self.temp_image = self.temp_image_folder / "tempimage.jpg"
        self.debug = False
        self.step_size = 4
        self.max_frames_ahead = 100

        # Dandere2xCPP
        self.dandere2x_cpp_block_matching_arg = self.service_request.output_options["dandere2x_cpp"]["block_matching_arg"]
        self.dandere2x_cpp_evaluator_arg = self.service_request.output_options["dandere2x_cpp"]["evaluator_arg"]


    def log_all_variables(self):
        log = logging.getLogger(name=self.service_request.input_file.name)

        log.info("Context Settings:")
        for item in self.__dict__:
            log.info("%s : %s" % (item, self.__dict__[item]))

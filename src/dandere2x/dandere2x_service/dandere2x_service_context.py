import logging
import os

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

        self.input_frames_dir = os.path.join(service_request.workspace, "inputs") + os.path.sep
        self.residual_images_dir = os.path.join(service_request.workspace, "residual_images") + os.path.sep
        self.residual_upscaled_dir = os.path.join(service_request.workspace, "residual_upscaled") + os.path.sep
        self.residual_data_dir = os.path.join(service_request.workspace, "residual_data") + os.path.sep
        self.pframe_data_dir = os.path.join(service_request.workspace, "pframe_data") + os.path.sep
        self.correction_data_dir = os.path.join(service_request.workspace, "correction_data") + os.path.sep
        self.merged_dir = os.path.join(service_request.workspace, "merged") + os.path.sep
        self.fade_data_dir = os.path.join(service_request.workspace, "fade_data") + os.path.sep
        self.debug_dir = os.path.join(service_request.workspace, "debug") + os.path.sep
        self.console_output_dir = os.path.join(service_request.workspace, "console_output") + os.path.sep
        self.compressed_static_dir = os.path.join(service_request.workspace, "compressed_static") + os.path.sep
        self.encoded_dir = os.path.join(service_request.workspace, "encoded") + os.path.sep
        self.temp_image_folder = os.path.join(service_request.workspace, "temp_image_folder") + os.path.sep
        self.log_dir = os.path.join(service_request.workspace, "log_dir") + os.path.sep

        self.directories = {self.input_frames_dir,
                            self.correction_data_dir,
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
        self.bleed = 1
        self.temp_image = self.temp_image_folder + "tempimage.jpg"
        self.debug = False
        self.step_size = 4
        self.max_frames_ahead = 100

    def log_all_variables(self):
        log = logging.getLogger(name=self.service_request.input_file)

        log.info("Context Settings:")
        for item in self.__dict__:
            log.info("%s : %s" % (item, self.__dict__[item]))

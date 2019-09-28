from dandere2xlib.utils.yaml_utils import get_options_from_section, absolutify_yaml
from wrappers.ffmpeg.videosettings import VideoSettings

import tempfile
import logging
import pathlib
import json
import math
import sys
import os


class Context:
    """
    This class is a mega-structure like file to house all the variables and directories needed for dandere2x to work.
    Rather than passing around the needed variables for dandere2x related functions, we simply put everything
    Dandere2x related in here and are loaded in various methods. You'll see this class become used a lot during
    D2x's development - keep this file clean and nice, as it'll be used more than anything else!
    """

    def __init__(self, config_file_unparsed: json):
        """
        Create all the needed values that will be used in various parts of dandere2x. A lot of these values
        are derived from external files, such as the json, ffmpeg and ffprobe, or are joined from directories.

        Having all the variables here allows dandere2x the values needed to be global, but at the same time not really.
        """

        self.this_folder = None

        # load 'this folder' in a pyinstaller friendly way
        if getattr(sys, 'frozen', False):
            self.this_folder = os.path.dirname(sys.executable)
        elif __file__:
            self.this_folder = os.path.dirname(__file__)

        self.this_folder = pathlib.Path(self.this_folder)

        # Parse the unparsed config into a parsed (../externals -> C:/this_folder/externals)
        self.config_file = absolutify_yaml(config_file_unparsed, str(self.this_folder.absolute()), absolutify_key="..")
        ################################
        #  setup all the directories.. #
        ################################

        # TODO: since this is a fail-safe method on loading the waifu2x clients
        # we gotta check at least one is ok before running dandere2x?

        if "waifu2x_converter" in self.config_file:
            self.waifu2x_converter_cpp_path = self.config_file['waifu2x_converter']['waifu2x_converter_path']
            self.waifu2x_converter_file_name = self.config_file['waifu2x_converter']['waifu2x_converter_file_name']
            self.waifu2x_converter_cpp_file_path = os.path.join(self.waifu2x_converter_cpp_path,
                                                                self.waifu2x_converter_file_name)

        if "waifu2x_ncnn_vulkan" in self.config_file:
            self.waifu2x_ncnn_vulkan_path = self.config_file['waifu2x_ncnn_vulkan']['waifu2x_ncnn_vulkan_path']
            self.waifu2x_ncnn_vulkan_file_name = self.config_file['waifu2x_ncnn_vulkan'][
                'waifu2x_ncnn_vulkan_file_name']
            self.waifu2x_ncnn_vulkan_file_path = os.path.join(self.waifu2x_ncnn_vulkan_path,
                                                              self.waifu2x_ncnn_vulkan_file_name)

        if "waifu2x_ncnn_vulkan_legacy" in self.config_file:
            self.waifu2x_ncnn_vulkan_legacy_path = self.config_file['waifu2x_ncnn_vulkan_legacy'][
                'waifu2x_ncnn_vulkan_legacy_path']
            self.waifu2x_ncnn_vulkan_legacy_file_name = self.config_file['waifu2x_ncnn_vulkan_legacy'][
                'waifu2x_ncnn_vulkan_legacy_file_name']
            self.waifu2x_ncnn_vulkan_legacy_file_path = os.path.join(self.waifu2x_ncnn_vulkan_legacy_path,
                                                                     self.waifu2x_ncnn_vulkan_legacy_file_name)

        if "waifu2x_caffe" in self.config_file:
            self.waifu2x_caffe_cui_dir = self.config_file['waifu2x_caffe']['waifu2x_caffe_path']

        self.workspace = self.config_file['dandere2x']['developer_settings']['workspace']
        self.workspace_use_temp = self.config_file['dandere2x']['developer_settings']['workspace_use_temp']

        # if we're using a temporary workspace, assign workspace to be in the temp folder
        if self.workspace_use_temp:
            self.workspace = os.path.join(pathlib.Path(tempfile.gettempdir()), 'dandere2x') + os.path.sep

        # setup directories
        self.input_frames_dir = self.workspace + "inputs" + os.path.sep
        self.residual_images_dir = self.workspace + "residual_images" + os.path.sep
        self.residual_upscaled_dir = self.workspace + "residual_upscaled" + os.path.sep
        self.residual_data_dir = self.workspace + "residual_data" + os.path.sep
        self.pframe_data_dir = self.workspace + "pframe_data" + os.path.sep
        self.correction_data_dir = self.workspace + "correction_data" + os.path.sep
        self.merged_dir = self.workspace + "merged" + os.path.sep
        self.fade_data_dir = self.workspace + "fade_data" + os.path.sep
        self.debug_dir = self.workspace + "debug" + os.path.sep
        self.log_dir = self.workspace + "logs" + os.path.sep
        self.compressed_static_dir = self.workspace + "compressed_static" + os.path.sep
        self.compressed_moving_dir = self.workspace + "compressed_moving" + os.path.sep
        self.encoded_dir = self.workspace + "encoded" + os.path.sep
        self.temp_image_folder = self.workspace + "temp_image_folder" + os.path.sep

        # put all the directories that need to be created into a list for creation / deleting.
        self.directories = {self.workspace,
                            self.input_frames_dir,
                            self.correction_data_dir,
                            self.residual_images_dir,
                            self.residual_upscaled_dir,
                            self.merged_dir,
                            self.residual_data_dir,
                            self.pframe_data_dir,
                            self.debug_dir,
                            self.log_dir,
                            self.compressed_static_dir,
                            self.compressed_moving_dir,
                            self.fade_data_dir,
                            self.encoded_dir,
                            self.temp_image_folder}

        self.ffmpeg_dir = self.config_file['ffmpeg']['ffmpeg_path']
        self.ffprobe_dir = self.config_file['ffmpeg']['ffprobe_path']
        self.hwaccel = self.config_file['ffmpeg']['-hwaccel']

        ################################
        # Load Dandere2x User Settings #
        ################################

        # User Settings
        self.block_size = self.config_file['dandere2x']['usersettings']['block_size']
        self.quality_minimum = self.config_file['dandere2x']['usersettings']['quality_minimum']
        self.waifu2x_type = self.config_file['dandere2x']['usersettings']['waifu2x_type']
        self.noise_level = self.config_file['dandere2x']['usersettings']['denoise_level']
        self.scale_factor = self.config_file['dandere2x']['usersettings']['scale_factor']
        self.input_file = self.config_file['dandere2x']['usersettings']['input_file']
        self.output_file = self.config_file['dandere2x']['usersettings']['output_file']

        # Developer Settings
        self.quality_moving_ratio = self.config_file['dandere2x']['developer_settings']['quality_moving_ratio']
        self.step_size = self.config_file['dandere2x']['developer_settings']['step_size']
        self.bleed = self.config_file['dandere2x']['developer_settings']['bleed']
        self.extension_type = self.config_file['dandere2x']['developer_settings']['extension_type']
        self.debug = self.config_file['dandere2x']['developer_settings']['debug']
        self.dandere2x_cpp_dir = self.config_file['dandere2x']['developer_settings']['dandere2x_cpp_dir']
        self.correction_block_size = 2

        # FFMPEG Pipe Encoding, NOTE: THIS OVERRIDES REALTIME ENCODING
        self.ffmpeg_pipe_encoding = self.config_file['dandere2x']['developer_settings']['ffmpeg_pipe_encoding']
        self.ffmpeg_pipe_encoding_type = self.config_file['dandere2x']['developer_settings'][
            'ffmpeg_pipe_encoding_type']
        self.nosound_file = os.path.join(self.workspace, "nosound")  # missing an extension, will set it in a few

        if not self.ffmpeg_pipe_encoding:
            # Real Time Encoding, traditional way
            self.realtime_encoding_enabled = self.config_file['dandere2x']['developer_settings']['realtime_encoding'][
                'realtime_encoding_enabled']
            self.realtime_encoding_delete_files = \
            self.config_file['dandere2x']['developer_settings']['realtime_encoding']['realtime_encoding_delete_files']
            self.realtime_encoding_seconds_per_video = \
                self.config_file['dandere2x']['developer_settings']['realtime_encoding'][
                    'realtime_encoding_seconds_per_video']

        else:

            # disable traditional "RTE" because we're piping
            self.realtime_encoding_enabled = False

            # get the substring after the last dot in the output_file "asd/aert/asd.mkv" --> "mkv"
            # but "important/rapgod" will default to rapgod.mp4 because we'll get
            # pipe_ext equals to the string itself "important/rapgod" and that's not an format :P

            supported_formats = [".mkv", ".mp4", ".avi"]

            pipe_ext = "." + self.output_file.split(".")[-1]

            # add the extension to nosound file
            self.nosound_file += ".mp4" if not pipe_ext in supported_formats else pipe_ext

        ##################
        # Video Settings #
        ##################

        # find out if the user trimmed a video by checking the time part of the json. IF theres nothing there,
        # then the user didn't trim anything
        self.user_trim_video = False
        find_out_if_trim = get_options_from_section(self.config_file["ffmpeg"]["trim_video"]['time'])

        if find_out_if_trim:
            self.user_trim_video = True

        # load the needed video settings
        self.video_settings = VideoSettings(self.ffprobe_dir, self.input_file)

        self.frame_rate = math.ceil(self.video_settings.frame_rate)
        self.width, self.height = self.video_settings.width, self.video_settings.height
        self.frame_count = 0

    # the workspace folder needs to exist before creating the log file, hence the method
    def set_logger(self):
        logging.basicConfig(filename=os.path.join(self.workspace, 'dandere2x.log'), level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def close_logger(self):
        logging.shutdown()

    def update_frame_count(self):
        """
        Count how many frames exist in the 'inputs_frames_dir' to signal to dandere2x how many frames
        will be needed during runtime. Observe that we don't use ffprobe's 'frame_count' function,
        as we we apply various filters which may affect total frame count.
        """
        self.frame_count = len([name for name in os.listdir(self.input_frames_dir)
                                if os.path.isfile(os.path.join(self.input_frames_dir, name))])
